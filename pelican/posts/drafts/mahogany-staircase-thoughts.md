Title: Thoughts on Ian Hickson's "Flutter's Layered Design" talk
Category: random thoughts
Tags: GUI, UI, Flutter
Date: 2018-07-17
Status: Draft
Summary: 

This post is basically unedited notes on Ian Hickson's "The Mahogany Staircase - Flutter's Layered Design" https://www.youtube.com/watch?v=dkyY9WCGMi0

- He went over how you don't *necessarily* need to represent your GUI as a tree - trees are an abstraction that makes layout easier.

- His presentation begins from the bottom up, starting with rendering primitives. I think this is the wrong way to think about UIs in general (though for this talk it may be the correct order). UIs should be thought about from the top down - ideally with some sort of markup like QML + state and APIs, layout ideally as a separate concern once you have defined your constraint model (flutter-style where constrains are part of the document model i.e. having Center and Align widgets or having seperate markup and using something like flexbox) and furthermore layout and rendering also being decoupled.

- 9:30 "having two places to update state", this is where most UI toolkits are at currently, Qt and GTK, iOS I think he mentioned as well, etc. Flutter and React instead are based on the idea of uni-directional flow of state. I believe this is why eventually he gets to the idea that the widget tree is immuatable but it's not clear why he thinks that.

- 10:40 his explanation of widgets and reuse for layout being complicated may be a symptom of the inherent complexity or may be a symptom that a foundational theory with which to explain the idea is missing

- 11:30 he hasn't explained why the widgets are immutable

* I believe they should be immutable *at render time* as in the part of Raph's talk about "splitting state" - but they should be mutable when state changes (and then set a "dirty" flag to invalidate layout cache)

	* this needs to be fleshed out more

- 12:17 "widgets as a description of configuration of render objects" yes and in fact we should go one step further and instead of "render objects" we should output a layout tree or sequence of layout primitives that can then be rendered by any backend. there should be the ability to then put in a caching layer here almost transparently. also needs to be fleshed out more.

- 12:50 the indirection of having an intermediary which holds refs to both the rectangle widget and the render widget just for comparison when doing caching is bad, both architecturally and for rust specifically. this could be solved with Ids like in raph's talk, or by some other mechanism.

- 13:20 "create a widget with its own render object" i should make one of those meme programmerhorror phone number selector interfaces that uses a custom widget which is a fidget spinner whose state is the number of times it's been spun in a given direction.

- 15:00 "if you made the widgets mutable, it would be no different than the render object layer" that is kind of what we want though, widgets describe two things: how to get input and how to draw the interface the user is using to get the input. we'll see what he says.

	- still on the above, he talks about how the element object between the render object has to recognize that the new widgets being passed in match the old render tree - i think this is dumb and i think raph's "state separation" solves this more elegantly. instead of getting the intermediary element to do cache invalidation, when we do our mutations to the tree we have to do them through something that marks the widgets as dirty.

- 19:40 again i think the "stateful builder" is a workaround instead of having the state mutable and the state being pumped through the tree to the widgets

- 21:00 okay now that i'm thinking about it, flutter does have "State" objects that kind of do what i'm talking about, they get pumped through via the setState method i think. maybe having stateful vs stateless objects is simply an optimization so that you don't have to pump state through all elements when most of the elements do not need any of the state. i.e. a red swatch at the top of the app will always be red.

	- I still think the talk is lacking the fundamental for why this is happening though

- 22:00 "State is anything that impacts how the application renders" yes and no. how the application renders should change based on state or your GUI is not properly displaying the state i.e. now your state is opaque to your users which is bad, but there can be state that isn't rendered, and the rendering is not the important part. the state is the parameters that are used for your actions.

- 23:00 so yeah he's very focused on state as being related to rendering, things that make you redraw. i really think it should be the opposite.

- 23:50 their definition of state to use as contrast for my definition

- 24:00 "where to put state" yes, I really want to know how he thinks about this because I don't have a great answer. redux "stores" seem maybe like an answer so I want to see how this is related.

- 26:00 so yes, the way that state works in Flutter is more bottom-up than top-down.

- At some point it was mentioned how things like screen orientation and image dimesions (i.e. whether an image has been loaded) is state. It is, but it doesn't really fit in to my "actions with paramters aka API" model of UIs, it's like "extraneous state" or "layout/rendering state". maybe in redux you would just call this another store. 

I do feel like there should be a fundamental difference between the state of a checkbox and the state of an image being loaded or not.

- 31:00 "stop walking a tree when you see a widget you've seen before" this is supposed to be an argument for immutability of the widget tree, but again I don't think it needs to be. I'm not sure about this still

- 32:00 "don't give affordances to slow operations" in particular making it hard to use non-cached text widgets is a nice idea

- 33:00 end of talk. overall flutter has a good model that i think is maybe lacking in a fundamental organizing principle or architecture but is definitely a big step in the right direction for GUIs. also talk is 2 years old, though i don't think that much has changed. I think there's more stuff that has been worked in with regard to state maybe.

- 36:00 in question about how does animation work, it describes why the bottom-up approach for state works. something pushes a tick update directly to the animation controller, which then does a set state (thus marking that part of the tree dirty). then we continue walking the tree and see nothing else has changed, so we stop walking the tree. that is, they only walk the tree for things that have changed state i.e. have updated.

This is the real reason for separate stateful vs stateless widgets. the state doesn't get pushed through the whole tree, it only gets pushed to the stateful widgets. so if we want to conceptually push state through the whole tree, we should instead figure out how to push it only to the ones that need updates. this is really just an optimization though - we keep track of which elements in the tree (which ids) actually want state changes, i.e. a cache.

After having watched this talk I'm going to watch a bunch of stuff about how React and Redux work and try to compare them. There's a lot of stuff on youtube about how to use them though, so it might be a bit difficult. I'm basically just googling the authors' names.
