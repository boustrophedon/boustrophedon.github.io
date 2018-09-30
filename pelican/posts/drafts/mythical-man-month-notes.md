Title: Notes from The Mythical Man-Month
Author: Harry Stern
Date: 1970-01-01
Category: Book Reviews
Tags: software development, project management, book reviews
Status: Draft

So basically nobody likes reading book reviews. I can't think of the last time I've read a book review about a non-fiction book. These are basically my notes taken while reading. Taking notes for books like this that aren't math/algorithms books helps me internalize more of the information and come back to review it later. I guess it's similar to the synthesis that happens when you do the exercises in a math textbook.

# 0 Many of the references and advice are dated

there's a section about how to use and budget space with a description of using tape drives vs core memory or something and how the latency from tape drives drove software to be better, and then when the hardware got better the software got worse.

this is basically what happened with javascript and 4GB+ chrome tabs.


# 1 The Tar Pit

## Software projects still fail a lot

Large scale "tar pits" still happen today - healthcare.gov and the UK's NHS healthcare project also were overbudget/failed. Programming 40 years later is still young.

## It's easier to build more complete programming products today

I think in some sense the distinction made about "programs" vs "programming products" are still useful, but in general it has become a lot easier to write and publish something closer to a "programming product" with a much smaller team because we have accumulated many existing "programming system products" already. In that sense, the "programming system product" classification is a bit outdated because new systems are created now by combining pre-existing products with a new solution.

That is, because we have general-purpose operating systems like Linux, and general purpose web servers like nginx, and web server frameworks in every language imaginable, turning a "program" that consists of some functions that interact with a database into a fully-featured, interactive website ("programming system product"), is a much easier feat.

On the other hand, producing products such that "every input and output conforms in syntax and semantics with precisely defined interfaces [...] it uses only a prescribed budget of resources - memory space, input-output devices, computer time" is much harder because of the generality of the systems that we build upon.

## It's still fun to program

The section called "The Joys of the Craft" is basically still true: it's still fun to program as an act of creation.

I'm going to try to make fewer notes that are just "yes this is still true", that said, it is also to some extent that programming also sucks sometimes, but I feel like we've made a lot of improvements so that it does not suck nearly as much if you use the correct tools.

# 2 The Mythical Man-Month

## Making estimates is hard

There was an article that I read some time ago about a company that specifically practices making estimates, and making them more accurate, using confidence intervals or something. I cannot find it now, but it is a contrast to the agile/kanban/whatever kind of software development practices that have emerged which have moved away from release dates and or making estimates at all.

I think I found it: the book was "How to Measure Anything" by Douglas Hubbard, but the only articles [like this one](https://www.lesswrong.com/posts/ybYBCK9D7MZCcdArB/how-to-measure-anything) like this one had no comments on HN.


## Optimism in programmers/programming

I feel like it isn't that all programmers are optimists, but that the [recency effect](https://en.wikipedia.org/wiki/Serial-position_effect#Recency_effect) makes it easier to be an optimist in the sense that once you get something working, you forget that it was difficult to get working. It was definitely the case for me for a long time. I would say recently, especially since starting to do "proper TDD", being conditioned to *expect* tests to fail first somewhat obviates the recency effect. I am also not sure that the recency effect is the right way to describe it.

## The mythical man-month


# ? surgical team model

why didn't this take off (to some extent)? part of it is that a lot of the staff was obviated by computers, but at the same time that means the programmer's/surgeon's time is also taken up entering non-code into computers.

additionally, a lot of open source projects kind of are like this: there are one or two main/core contributers, and a long tail of secondary contributers that kind of take up the "secondary" work. it would be nice if more people specifically did this "secondary/bookkeeping" work but if you're volunteering your time, you want to work on the fun stuff.

Steve Klabnik does a lot of this "secondary" stuff, especially wrt documentation, for the rust project.

# 10 Documents

"objectives" are mentioned as a document for a software project, with the "goals, desiderata, constraints, and priorities". OKRs are a way to structure this. :)

Some of the stuff about budget and market and forecasting is very focused towards "product development" in the "lean startup" sense: there is an existing market with existing customers and you want to deliver an improvement or incremental offering. that specific advice probably isn't as useful for startups.

# 11 Throw one away

"The management question, therefore, is not whether to build a pilot system and throw it away. You *will* do that. The only question is whether to plan in advance to build a throwaway, or to promise to deliver the throwaway to customers.

## Embrace change

iterate and pivot

## reluctance to document

From a reference by Cosgrove, unsure of the exact reference
"By documenting a design, the designer exposes himself to the criticisms of everyone, and he must be able to defend everything he writes. If the organization structure is threatening in any way, nothing is going to be documented until it is completely defensible"

google did multiple studies about a similiar effect: feeling psychologically safe and supported by teammates, not being afraid of criticism, was one of the most important factors in what makes a good team.

## "bugs found" curve

p 121, graph depicting bugs found vs months since installation of a particular release of software. it starts off high as you can imagine, and decreases over time (this is a section about program maintenance) but then after a while the number of bugs found increases.

# 12 Sharp Tools

this is a juicy one. "Even at this late date, many programming projects are still operating like machine shops so far as tools are concerned. Each master mechanic has his own personal set, collected over a lifetime and carefully locked and guarded - the visible evidences of personal skiils. Just so, the programmer keeps little editors, sorts, binary dumps, disk space utilities, etc. stashed away in his file."

The following sections about having teams or at least people devoted to building tools to enhance other programmers' productivity, even though the specifics of the tools mentioned are very outdated, is strongly embodied at a lot of the current top technology firms.

However, the reasoning is kind of different. Personal utility code sets and tools aren't really a thing anymore, but there are so many tools now: programming languages, editors, debuggers, operating systems, deployment frameworks, etc., that a programmer is now categorized by the knowledge they have of these specific pre-existing tools. The specific tools you use are not nearly as important and take a relatively small time to learn compared to the specifics of the actual software you are building. 
