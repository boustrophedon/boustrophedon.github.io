Title: How to format your entire codebase without introducing backdoors
Category: Programming
Tags: trusting trust, programming, git
Date: 2021-05-14
Status: draft

When working on legacy code with many developers, it's pretty common for someone to suggest running a code formatter on the whole codebase. Even small code formatting changes often get called out in code review for making the code harder to review. Why don't we automatically format our code?

The fundamental reason why this is a problem is that it's basically impossible to review the changes since they're likely to hit every file in your codebase. It would be very easy to introduce, for example, a hidden backdoor, and you also can't verify if, due to configuration differences, the formatting simply isn't as agreed upon without further systems in place.

So how do we take a codebase without consistent style and make it pretty?


## Step 0: Make a decision as a team to format the code
If you're working as a team (if you're the sole owner of your code presumably you can trust yourself to not introduce backdoors) you need to agree on what code style and formatter you're going to use. Try not to bikeshed too much and use the defaults your particular tool has.

## Step 1: Make sure that code formatting is required on all future commits.
You must have an automated step in your review process or build pipeline to check that the code is formatted properly. If you don't do this, you'll eventually end up where you started: inconsistent formatting, unreadable test names, and needless clashes over style in code review.

You may be able to enable this prior to actually formatting the rest of the codebase if your tool is able to process only diffs, but if not you will need to enable it immediately after committing the formatted code.

In fact, **you may be able to stop here!** If you trust your CI system, it may be sufficient to post the code review and have your reviewers note that it passed the formatting check in your pipeline. If it isn't possible to do this or you would like to have more confidence, keep reading.

## Step 2: Document the steps you will take to format the code

This may be as simple as "run command X in the root of the repository" or an entire script. Be sure to include any configuration files for the formatter! This should be pretty easy, as it should be the same as your automated system's setup.

## Step 3: The Formatting Ceremony

This is the interesting part.

Similar to a [key-signing party](https://en.wikipedia.org/wiki/Key_signing_party) or the [Root DNS key signing ceremony](https://www.cloudflare.com/dns/dnssec/root-signing-ceremony/), decide as a team who you trust to make the changes, have them gather in a room (or use pre-shared gpg keys to sign the commits if you are fully remote), and have them all run the same steps to format the code.

Then, by sharing the code (pushing separate branches to a shared repository, transferring via USB drive, or carrier pigeon), have each member diff their formatted code against the others' and check that there are no deviations. If you're remote, make sure to check the signatures on each commit with `git log --show-signature`.

If everything checks out, pick someone at random to send out the pull request and have the other ceremony participants sign off after checking the commit id (and signature) matches the ones checked locally, hopefully in addition to the newly-added automated formatting check.


## Remaining issues and alternative solutions

The biggest issue with a large formatting commit is that the output of `git blame` and to a lesser extent `git log` are obscured. Because your formatter will very likely touch a large percentage of the lines in your codebase, running `git blame` will show you the formatting commit as the most recent commit, instead of actual code changes, on most lines.

There's a [good article](https://www.moxio.com/blog/43/ignoring-bulk-change-commits-with-git-blame) describing a relatively recent feature of git which lets you configure a file (or command line parameter) listing commits that git blame should ignore. As noted in the article, most tools, like GitHub and GitLab, do not support this feature yet.

Also, there may be a way to streamline the verification process if you're meeting physically in the same place, by doing some kind of variant of the [Zimmermann-Sassaman key-signing protocol](https://en.wikipedia.org/wiki/Zimmermann%E2%80%93Sassaman_key-signing_protocol) used at key-signing parties.

### An alternative and gradual but more annoying solution

There is an alternate, but more annoying way to make these changes without a single big commit, and without obscuring the git blame.

You can run the code formatter per-diff, only on the code that has been changed. As your codebase is worked on, it will gradually be formatted. This can work if it's constantly under change, you have a lot of large commits and rewrites, or your codebase is mostly pretty clean and you just want to enforce the standard for new code only. There are cases where this will not work, if for example you want to change indentation style in Python or if your formatting style requires a specific method/class/variable naming convention and your commits do not touch all uses of the name.

The main downside of this method is that your codebase becomes partially-formatted, which may make it more unreadable than it was before.

The other downside of doing the formatting partially is that if you want to make this process automated, your formatter has to be able to work on diffs, which is not a particularly common feature. You may have to format the entire file and then use features of `git add` to only add the specific lines you want, which is annoying.

## Summary

- Agree to require code formatting on all commits
- Make it automated
- Gather trusted people in a room, or have them exchange gpg keys over a trusted channel if remote
- Everyone runs the same steps to format the code, exchanges the resulting commits, and verifies that
  - The commits are all the same
  - The signatures match (if working remotely)
- Randomly choose someone to push the code for review
- Everyone again verifies the code in the review matches their own diff, and approves the code
- Enable a formatting check in your CI pipeline / code review tool
- Use `git config blame.ignoreRevsFile` with a file that contains the formatting commit id to ignore it in `git blame`

I honestly don't know how many projects this is actually useful for: it's mostly written to try and convince my coworkers to do it for our codebase. I think you would get objections to doing this if you were even a mildly popular open source project.

I'd love to hear about alternate methods to do this, or if you've successfully done something similar in your own codebase as a datapoint for implementing it at work. 
