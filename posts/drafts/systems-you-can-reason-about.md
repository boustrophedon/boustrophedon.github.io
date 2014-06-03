title: systems you can reason about talk gerald sussman
Date: 2018-10-21
Status: Draft

https://www.infoq.com/presentations/We-Really-Dont-Know-How-To-Compute

this talk consistently blew my mind both on how smart gerald sussman is and how shitty modern computation is.

https://www.youtube.com/watch?v=ubaX1Smg6pY

the very next talk that i started watching (both i found from this HN thread: https://news.ycombinator.com/item?id=18217762) featured none other than alan kay talking about very very similar ideas.

the core idea in both talks is that a "good system" is one you can reason about and query. both of them might disagre, but this is the core idea that i got out of it. okay, in both of their talks they also emphasized the conciseness of their systems and how they are built from small parts, but i don't think anyone really *intentionally* builds systems that are big and unwieldy: they just turn out that way because of poor design.

in sussman's demo (using lisp) he showed systems that took in varying bits of local information, and combined them with given constraints to deduce more information. the examples he gave were taking various measurements about a building to get its height, and then being able to reason backwards from the resulting estimate to see which caused the measurements. additionally, he showed a system to reason about electrical diagrams, which computes various voltages or whatever, and gives you the ability to reason about it: what computations give us the result? if i change this value, how do the others change?

in kay's demonstration, he shows a graphics system by Dan Amelang (Nile) and Bret Victor (unnamed demo?) which allows you to query both forwards and backwards the result of drawing graphics primitives: what operations and primitives lead to the drawing of this pixel?

The "slide" at about 1:14:00, in contrast with all the concise programs he showed up to this point, made me realize that basically all the work people do to make the things on the bottom, i.e. writing big systems like word or openoffice or firefox, are the equivalent of manually unrolling the dynamicism in a dynamic system. That is, the way he was able to eg. dynamically change the gradient on an individual widget in his system is something that you would have to manually program in, in a system like eg Flutter or a web browser.

also, the idea of a "semantic compiler", and the thing he mentioned earlier at about 1:10:00 regarding a "semantic negotiation process" (maybe as an example of/lead-in to a semantic compiler). this is basically how sci-fi systems work. "i'm sending the data to your terminal" -> the main character looks down at a hologram from his hand or a display on his arm and sees it there. *something* makes the data interoperate and display nicely between all these various sensors, inputs, outputs, networks, etc. and in kay's world it's called a "semantic compiler/negotiatior"

holy shit i've known the story of jacob and esau since i was a kid but i have never made the connection that alan kay makes: it's not about "making a poor deal" it's about humanity's impulsiveness and our willingness to give up what's important for convenience.
