Title: "Containerize" individual functions in Rust with extrasafe
Date: 2023-04-04
Slug: extrasafe-user-namespaces

# Extrasafe now has namespace support

Today I released a new version of [extrasafe](https://github.com/boustrophedon/extrasafe) which has support for using [Linux's namespaces feature](https://man7.org/linux/man-pages/man7/namespaces.7.html) to create browser-style content processes. Namespaces are perhaps more famously used in container runtimes, which is why I used them in my clickbait title, but the main inspiration and use-case for extrasafe's Isolate is closer to a browser's content process.

Extrasafe is a Linux security toolkit for Rust that makes it simple to use kernel security features directly inside your Rust code. Extrasafe already has support for seccomp and Landlock, which are also used in browsers, containers, and other kinds of isolation tools like firejail and bubblewrap.

The `Isolate` feature I'm releasing today lets you run individual functions inside unprivileged user namespaces.

## Overview

Fundamentally extrasafe's namespace support works mostly the same as a typical container runtime:

- At some point in your code, call `Isolate::run`
- Create a memfd and copy /proc/self/exe into it (this protects the original executable from being modified)
- Use a standard `std::process::Command` to exec `/proc/self/fd/<memfd>` with an argv[0] that indicates to extrasafe we're a content process
- Back in main, hit the `Isolate::main_hook` call
- Allocate a new stack
- Clone with `CLONE_NEWUSER`, `CLONE_NEWNS`, etc flags to enter a new namespace (often fork + the unshare syscall are used instead)
    - the `CLONE_PIDFD` flag is also used
- Map the current user into the namespace as root
- Mount a new tmpfs and bindmount anything the application needs into it
- Call the `pivot_root` to switch to the filesystem set up previously
- Unmount the old root mount
- Clear all fds except for stdout and stderr
- Run the user-provided function and exit when it's done
- In the process spawned by Command, wait on the pidfd provided by clone.
- In the original process, wait on the new process with the `Command::output` method to gather any output

We exec (see discussion below for why we have to exec at all) prior to `clone`/`pivot_root` because otherwise the linker may not be able to find the necessary .so files to link to if the program is dynamically linked, even if we kept a fd with the contents of `/proc/self/exe` around. This sequence of operations requires that we have something like `Isolate::main_hook` to do the setup, and adds an extra point of failure in the sense that a user might not call it. It's not really an issue because in that case the program wouldn't make it to the code to be isolated anyway, but it makes the overall experience more complicated.

Also, one random fact I discovered while working on this feacture that doesn't seem to be documented anywhere besides [a random git commit message in systemd](https://github.com/systemd/systemd/commit/b71a0192c040f585397cfc6fc2ca025bf839733d): In order to mount a proc or sysfs filesystem inside a user namespace, you must already have a proc (or sysfs) filesystem mounted in your tree somewhere.

## Use-cases

At my previous job we had a separate internal service for converting and transforming image data because of issues with CVEs in imagemagick and similar image-parsing libraries. While it may make sense from a deployment and scaling perspective to do so regardless (because doing image ops is more computationally intensive than serving web requests, for example), using something like the equivalent of a browser's "content process" to isolate CVE-prone libraries could be an operational and performance (esp. latency) win in some cases.

Other similar tasks you might want to use an extrasafe Isolate for are things like: running ffmpeg, calling into closed-source binary libraries (another thing from my last job), and possibly GPU stuff - in particular I'd like to write a gpu example based on chromium/firefox's content processes.

## Design choices

Like the rest of extrasafe, the design choices were made to make the implementation as simple as possible and the features simple to use and hard to misuse, not to provide all features of the underlying security tools.

### Clone vs fork

Using libc's clone wrapper rather than fork+unshare means that you get to start with a completely clean stack. Using fork makes it easier to pass data from prior to clone to the new process because you have all the existing stack variables, but it's not that hard to shove everything into a Box (which puts the data on the heap, which is copied to the new process), and then use libc's clone wrapper data pointer to access it again after the clone.

### When to exec

The biggest design choice that I wasn't sure about was to exec "first" (before entering the user namespace) or exec "last" (after doing all the setup but before `pivot_mount`), and the related issue of closing stdout/stderr or not. In the end I decided that re-using the std lib's Command made the implementation a lot simpler, and I don't think the tradeoffs are that bad. The biggest issue is in the setup code: execing first means the Isolate's config/setup data has to exist without the context of the code when `Isolate::run` is called, whereas execing "last" (i.e. right before we `pivot_root`) means that we can pass the Isolate's configuration data in memory from the point of starting the isolate all the way to after we're in the namespace.

With the current design, it forces you to come up with all of the configuration data at the start of the program, without any context of the rest of the program. This is nice because you have less to reason about in terms of state at startup inside the isolate, but can make usage more confusing. For example, if you have a config file that gets passed in the command line which contains a directory you want to bindmount into an isolate, you must first parse the CLI args, read the config file, get the directory, run the isolate, passing the directory as an environment variable to be used at isolate setup.

However, the isolate code that uses that environment variable will go *before* the above CLI/config parsing code in main (because the associated cli args aren't there in the isolate process). However, since the environment variable doesn't exist in the original process, the setup code must be gated on whether we're inside the Isolate already or not. That is why the second argument to `Isolate::main_hook` is a function: it only gets called and does setup if `main_hook` first detects we're in an Isolate.

This decision is one I would reconsider if someone came up with a use-case that the current design doesn't work well with.

Relatedly, there's no way to communicate between the parent and worker by default, which is also something I went back and forth with. In the end it's easy enough to set up a unix socket for communication, and pipes can be complicated (they can clog!). There's an example of using a unix socket for communication in `examples/isolate_tests.rs`.

### Filesystem consideration

By default the isolate creates a new tmpfs on top of a temporary directory created by mkdtemp, but I also considered just having the user provide a directory. I thought people might just give `/` though which kind of defeats the purpose - if you want a full OS container, just use docker or podman or whatever.

### Not execing at all?

This isn't really a design choice since I don't think there's an alternative but it would really be nice if we didn't have to exec and do the main hook thing, but execing:

- Lets us protect the original /proc/self/exe on disk via the memfd trick
- "Cleans" the memory space so no data in memory from prior to entering the isolate is available to the worker
- env and argv can be sanitized (env from program start can be accessed at /proc/self/environ even if you modify it in-process)
- Lets us take advantage of std Command's code that replaces stdout/stderr with pipes and reads them to strings rather than have to write it ourselves.

so I don't think there's a way around it.

### Network

I considered not even including the option to not create a new network namespace because in order to do HTTP, you most likely need to bindmount at the very least `/etc/resolv.conf` for DNS, and depending on your openssl situation `/etc/ssl` and similar directories (I spent a couple hours unsure why statx was failing on `/etc/ssl/cert.pem` when it was bindmounted via `/etc/ssl/` but not when I mounted the whole `/etc/` until I realized it was a symlink to a file in `/etc/ca-certificates/`). Using reqwest with the `rusttls-tls` feature makes it simpler because it bundles the certificates, but there can still be issues with DNS depending on how it's configured.

Ultimately the reason I kept the option is because even with the above DNS/SSL issues, it could be useful to isolate something and have it speak with a daemon that listens on a local IP port - not everything speaks unix sockets.

### Testing

Due to the way cargo's test runners are set up, I couldn't figure out a way to get Isolates to work with `cargo test`. So `examples/isolate_test.rs` just manually asserts and doesn't have a pretty output format, and is run separately in CI from `cargo test`.

Isolates also make coverage collection more difficult/impossible, but code coverage was already hard for extrasafe. Currently I'm using llvm-cov but it might be worth trying out tarpaulin again, which is ptrace-based.


## Future work

### Isolates

A proc wrapper macro for main instead of `Isolate::main_hook` would be nice.

Also, instead of using strings to link Isolate startup in `run` and usage in `main_hook`, it would be nice to use some kind of unique token manufacturing technique with some type system trickery. Initially I prototyped a hack where you could pass either a string or a unit struct using a std hasher and the hashes of the object itself and its type id, but I wanted to just release the feature already so I stayed with String ids for the time being, since you need the string for argv[0] regardless.

I'd also like to add a `mount_proc` option that bindmounts the parent proc inside the isolate, mounts a new proc, and then unmounts the original proc. This is already possible so I didn't think I needed to include it in the original release, but it would be nice as an option. There's a demo of this in `examples/isolate_test.rs` - as mentioned previously, you can't mount a proc fs without having one already mounted, so there's a bit more setup than just calling mount.

I don't know how hard it would be to add support for bridging just the loopback interface so that programs that don't want to have external network access but would prefer to communicate with the Isolate via TCP or UDP, but it would be nice to have. It feels like it would be a lot of work.

#### Issues

For some reason strace doesn't like the tests in `examples/isolate_test.rs` that panic in the isolates. They complete normally when run outside of strace, but if you run strace on the test binary, the isolate process segfaults in some kind of loop after recieving a `SIGABRT` via tgkill, segfaulting, and then resetting(?) the segfault signal handler.

### Other security features

The last remaining major security feature to add to extrasafe is [capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html). After entering the isolate, by default the user has the `CAP_SYS_ADMIN` capability inside the new namespace (it has all capabilities) which can be useful, but we'd also like to be able to drop it if we don't need it.

cgroups support is also a possibility but for the current use-case I'm not sure it wouldn't be better to configure it external to the program (e.g. via a systemd unit file). cgroups does allow you to, for example, set limits on processes which might help prevent DOS attacks, but you can also just use seccomp to stop the program from forking at all once you're in the isolate.

It would also be nice to document how to use bindmounts etc to access the gpu, as mentioned above, without just bindmounting the entire sys and proc directories from the host. I'm sure there's docker images from nvidia or someone that would be useful to take a peek at.

## Thanks for reading

If you've read this far, *I am looking for a new job*. If you'd like to talk, please reach out to me via email at \<my first name @ this domain\>
