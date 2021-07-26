Title: How to pair program like it's the 1980s (with GNU Screen)
Date: 2021-07-26
Status: Draft

## What we're doing

Suppose you want to pair program with someone remotely. You could use one of several online in-browser services or IDE plugins, but if your environment is special or you need access to some resources behind a VPN, these solutions may not work for you.

Screen is a tool originally from 1987 that allows you to run multiple terminals in one session. It's particularly useful on servers, where you can leave your session running after disconnecting in the same way that when you put your laptop to sleep, all your windows are still there when you open it back up. Tmux is a similar (but released 20 years later and so makes a less interesting title) program that's also popular.

We're going to use screen's multiuser feature to share the same screen session across two ssh sessions, letting two people interact remotely with the same shell at the same time. You could pair program by having each person type alternating letters if you really wanted.

## Why

Why not. Maybe you don't like screensharing because your Spotify playlist is full of Taylor Swift, or your OnlyFans notifications will give away your secret NASCAR hobby. Maybe you're actually swapping who's typing frequently. Maybe you can't program without your One True Vim Configuration.

## Prerequisites setup

To make this work you need to have access to a shared computer that you can ssh into. You can set this up with a single user (requires less configuration but not always ideal or possible, especially in corporate environments), two existing users if you're on a corporate or educational network and you already have shared access to several machines, or you can make an extra "guest" user and generate ssh keys per-guest, giving you the ability to revoke access easily.

In the first case (one user), you would just need to generate a new ssh key via something like `ssh-keygen -t ecdsa -C "pair programming key $(date +%F)"`, add it to your user's `authorized_keys` file, and give your friend the public key. Then all they need to do is ssh to your machine (on the same user as you) and use `screen -x` to attach to your screen session, without doing the extra setup for multiuser below.

Additionally, there is information on the internet about SELinux needing to be enabled but that doesn't seem to be the case on my desktop or server that I tested on. The screen binary also must be suid root but that was already the case on my server and desktop as well. I suspect both these issues may have been Ubuntu-specific.

## Screen basics

The most basic usage of screen is just to type `screen`, which creates a new session. You can then use `C-a c` to create a new  terminal, and `C-a a` to switch back to the previous one. You can use `C-a n` to go to the next in order and `C-a p` to go to the previous.

`C-a d` *detaches* the current screen, leaving all your terminals running and ready to be re-opened later. Note that if you put your laptop to sleep or shut your computer down, they will of course also pause or be terminated - it's not magic.

To resume a session, from a terminal we can run `screen -r`.

I typically run `screen -Udr` to resume a session, where the `-U` enables Unicode, and using `-dr` instead of just `-r` will detach other currently attached terminals. This is useful if you were attached via a laptop and want to attach from a different computer, or simply if you're lazy and don't want to find whatever other terminal is attached.

## Execution

There are a few parts:

1. We need to give our screen session a name so it's easy to join
2. We need to enable multiuser mode so other users can join
3. We need to give the specific user we want access to the session
4. The other user needs to attach to the shared session

Incidentally, the third point is why it may be easier to make a guest account for pair programming on your machine, because then you can give that guest account access permanently as we'll see later.

### 1. Naming a session

When starting a screen session, we can name it with the `-S <sessionname>` argument. Combined with the unicode flag above, it would look like `screen -US shared`, for example.

### 2. Enable multiuser mode

To enable multiuser mode, type `C-a :multiuser on`. Once you hit `:` after `C-a`, it will appear in the bottom left where the status messages appear, and as you type the rest it will show up there.

### 3. Give the other user access to the session

To give the other user access to our session, type `C-a :acladd <username>` where `<username>` is the name of the user's login on the machine, e.g. `guest` or `harrystern`.

### 4. Attaching to the shared session

Once your friend has sshed to your server, all they need to do to join your session is use the `-x <user>/<sessionname>` flag instead of `-r`. So as before with the `-U` flag, the full command would look something like `screen -Ux harrystern/shared`.

They should now see whatever you see on your terminal, and vice-versa. Anything you or they type *in the same terminal* will be shared, but you can open separate terminals with `C-a c` and view and use them separately. That is, the terminals themselves are shared but displaying them are not - you can view and type in one while your friend works in another, and switch between them freely. You just need to be careful about not accidentally typing when you're in the same terminal as someone else when they're working.

## Using `.screenrc` for streamlined shared access

In order to make this process easier, you can put some commands in a `.screenrc` file so that you don't have to do the permissions setup each time. Depending on your security requirements and level of trust, this may or may not be viable in your personal situation. e.g. I would not necessarily do it on a shared university machine, but I don't see an issue doing it on a secure corporate cloud machine where only other developers *may* have ssh access.

You can just open `~/.screenrc` with your favorite text editor and add the lines `multiuser on` and `acladd <username>` as we did in steps 2 and 3 above. Then all your screen sessions will be multiuser-enabled and available to join by anyone whom you've given access to via `acladd`.

Using `.screenrc` to manage access also makes it easier to use screen's advanced multiuser acl features, like enabling read-only access. See the man page for more information.

## Credits

I used [this page](https://wiki.networksecuritytoolkit.org/index.php/HowTo_Share_A_Terminal_Session_Using_Screen) to remind myself how to do this, and really the reason I wrote this post is so that I don't have to find that page or one like it in the future when I forget.
