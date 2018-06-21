Title: OKRs are just TDD for project management: "Measure What Matters" by John Doerr
Category: Book Reviews
Tags: OKRs, TDD, project management, book review
Date: 2018-06-18
Slug: okrs-are-tdd
Summary: I've been reading "Measure What Matters" by John Doerr, which is about OKRs and how to use them, and realized while reading the book that OKRs are similar to TDD. Also, there's a rant about how YouTube doesn't know what it's doing.

# Overview

I've been reading "Measure What Matters" by John Doerr, which is about using [OKRs](https://en.wikipedia.org/wiki/OKR) effectively. "Objectives and Key Results," or OKRs, are a framework for tracking goals and their progress in a project or organization. In this framework, Objectives are the goals you want to achieve, and Key Results are the (measurable) tasks that are necessary and sufficient for the goal to be completed.

The book is written in what I can only describe as a very business-school textbook style. The first half's chapters explain how to use OKRs, and the second half describes "applications and implications for the new world of work" which I would just describe as "other related stuff". It's very well written, and the case studies are the right length to break up the more textbook-like sections without themselves being overly monotonous.

Reading the book has definitely sold me on the usefulness of OKRs, whereas before I was kind of ambivalent on them. When I first encountered them as an intern at Google, they were only really half-explained - we were told what they were but not the why (or maybe we were and I just didn't pay attention!). Looking back, I definitely had better OKRs for my first internship than my second, which correlates with being more successful in my first internship than my second, though there were many reasons why my second internship was not successful.

I actually now think this book, or at least the summary at the end, should be required reading if you're going to use OKRs. Although the core idea is simple, the book expands on the idea and consequences: setting your goals ambitiously (stretch), focusing and narrowing down your goals to something achievable (focus and commit), how to align OKRs up and down the organization (align and connect), how to grade OKRs (track for accountability).

# Example OKRs

Some of the examples in the book aren't actually that great, mostly in terms of the measurability of the key results or the certainty with which the objective is complete given the completion of the key results, but here's a very simple one about hiring in a company.

#### Objective:

Support company hiring.

#### Key Results:

1. Hire 1 director of finance and operations (talk to at least 3 candidates)
2. Source 1 product marketing manager (meed with 5 candidates this quarter).
3. Source 1 product manager (meed with 5 candidates this quarter).

Here is an example from my personal OKRs for this summer, where the "complete three projects" is then a new objective with its own key results elsewhere:

#### Objective:

Improve resume and interviewing skills

#### Key results:

* Complete 10 blog posts by August 31, aiming for 1 per week
* Complete three projects to add to resume
* Complete 10 interviewing.io interviews by August 31, aiming for 1 per week
* Read at least half of cracking the coding interview

# OKRs as TDD

The realization that OKRs are just test-driven development for project management is what really solidified their usefulness for me. I haven't actually read a book on TDD (though I probably should), but I think that in the same way that TDD ensures you're writing code that does what you actually want, OKRs tell you whether you are achieving the goals you actually want. In particular, *you don't do things that don't contribute to your objectives* in the same way you don't write code that doesn't turn a test from red to green.

If you want to make the analogy more explicit, you might try saying that objectives = the code you write, and key results = the tests you write. Then you can tell you are writing the correct code (or achieving the goals you set) by seeing that your tests are passing (or that your key results are green). There is more to OKRs than just "tests and code", and if you wanted to extend the metaphor you could maybe make a connection between integration tests and aligning OKRs across teams and stuff, but I think the base comparison is enough to sell most developers to at least think about it more. And if the developer doesn't write tests, well, there's no saving them. (they'll figure it out eventually)

# Problems with OKRs: YouTube case study

OKRs are not a panacea, however. Among the many things cautioned against in the book, probably the most important are choosing the wrong objectives and choosing too many objectives. In fact, it wasn't poised this way, but the YouTube case study kind of highlights what happens if you choose the "wrong" objectives. The YouTube case study ranges over several people at various levels of leadership, but the thing that stuck out to me was the way that the objectives changed. To me, the changing objectives seems to say that they haven't found the right objective. Sure, you can argue that the "correct" objective can change over time, but in this case the objectives were changing for seemingly arbitrary reasons.

There is a very indicative quote about the switch from views to watch time as a key metric: "Our job was to keep people engaged and hanging out with us. By definition, viewers are happier watching seven minutes of a ten-minute video (or even two minutes of a ten-minute video) than *all* of a one-minute video. And when they're happier, we are too." YouTube has been *consistently* criticized for its changing standards and opaque processes. Video creators intentionally put useless filler in their videos to reach 10 minutes, to the point where [it's essentially a meme](https://www.urbandictionary.com/define.php?term=10%20minute%20ad%20revenue) to add some extra frames at the end of a video to make it exactly 10:01. In the past, [reply girls](https://en.wikipedia.org/wiki/Reply_girl), [bizarre "kids'" videos](https://en.wikipedia.org/wiki/Elsagate), in addition to all the various [copyright issues](https://en.wikipedia.org/wiki/YouTube_copyright_issues), including the deletion of [videos documenting atrocities in Syria](https://www.nytimes.com/2017/08/22/world/middleeast/syria-youtube-videos-isis.html) and today [taking down MIT OCW and Blender Foundation videos](https://www.dailydot.com/debug/youtube-mit-opencourseware-blender-foundation-blocked/) have all contributed to the general feeling that YouTube doesn't care about its users. (I feel that after compiling all this criticism, I should clarify that I love YouTube and have probably contributed thousands of hours of watch time since 2005, and I'm only saying these things because I care.)

This problem is also a specific instance of the problem that, although the various groups in the organization may have aligned their objectives, the objectives are not aligned with their users. Later in the book, in the section about Bono and his organization, John asks them "Who is the client? Do they have a seat at the table?" In the case of YouTube, well, they claimed in their OKRs that they want to "delight users", but it didn't sound like their users had a seat at the table. In fact, the biggest complaint about Google is that there's no way to talk to them. Some teams do talk to their users (Fiber and Flutter being two that I personally know of), but others are big black boxes. Now, if you take the view that YouTube's *customers* are the advertisers and not the users or content creators, many of the actions they take make some sense. I personally think that kind of thinking is the tail wagging the dog, though. In contrast (this entire section should be a separate post at this point so I'll be brief), Twitch's goals are much more aligned with their users: higher watch times translate directly to more user happiness and more money for streamers, and all of the monetized features benefit the user, the streamer, and Twitch itself (with maybe the exception of Twitch Prime, which is just Amazon spending money to increase retention).

# Aligning OKRs throughout an organization

As I was reading the book, I was having a hard time understanding how you effectively communicate your OKRs across teams to align objectives. If everything cascades down directly from the top, everything is aligned, but as is explained in the book, this prevents ideas and problems from being transmitted upwards, and can make it difficult to effect rapid change.

Near the end of the book in one of the case studies, it mentions how one company eschews the use of green yellow red grades, and instead has just green and red. They have a monthly review, and greens are mostly ignored. It's a bit unclear how they actually make and grade the OKRs (usually grades are given retroactively, so perhaps their objectives are e.g. quarterly and the KRs evolve monthly? and this takes place after grading the previous month's KRs). The owners of the "red" OKRs then "sell" i.e. present why their OKR is at risk, and then everyone votes on which are the most important, and people volunteer to "buy" other teams' reds. This seems like a very effective way to communicate and align goals across different parts of an organization and I'm a bit surprised it's somewhat buried towards the end. The whole "buying"/"selling" thing is a bit superfluous but the idea seems great.

# OKRs are not specific to corporations

The last thought I have on this book is that, although almost all the testimonials are from corporations and the language is heavily management-coded, the core principles are not specific to corporations. Nonprofits, open-source projects, and research teams could all benefit from having clear goals and enumerated, measurable subgoals to achieve the objectives. If you really wanted, you could use these ideas to work on a group project in a high school class.

Anyway, try it out.

###### *Shoutouts to Allen, Tim, and Wayne for reading drafts of this post*
