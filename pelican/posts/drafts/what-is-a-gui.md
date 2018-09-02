Title: Is there a theoretical foundation for GUIs?
Date: 1970-01-01
Status: Draft

# What is a GUI?

Graphical - you have to draw a GUI i.e. layout

User Interface - you have to take user inputs and do something with them

okay that's pretty dumb. but yeah, the basic thing that a GUI does is draw some things, then when the user interacts with the things, some state changes.

Usually, the state is one of two things: either a value is updated that is used by the program (and should also be displayed by the widget), or it triggers a state transition in the GUI itself - a screen change, a popup 

I want to basically get at composable finite state machines - each widget is a finite state machine, and you can take their product which is just a bunch of states, but you should also be able to take a "sum" of some sort, where a transition in one widget causes a transition in another widget.

essentially we either change state, or perform an action. many systems turn "change state" into "perform an action" by making all state changes events.

features that nice to have: "hot reloading", "time travelling"/replays,
	- data driven architecture and QML-like interface allows you do to hot reloading even with statically typed and compiled languages to some extent. to go even further maybe look at what flutter does to get that dynamicism on compiled platforms like ios
	- the way react hot loader works is to replace the actual actions with a dispatch proxy, and then has some sort of code that manages the reloading of the proxy. this could be done with some effort via dynamic linking

layout and rendering are not the whole world! half of a GUI is the user interface, the interactive part of communicating with the user.

redux seems like it actually is just finite state machines, where the state is in the store and actions are transitions. your reducers are just the implementation of what the transitions do.

# Things we want

- Separatation of layout and rendering (like yoga or cassowary)
	- Ideally layout simply outputs a bunch of things to render, ideally just the diffs from the previous frame
- "Unidirectional flow of state" or whatever it is that redux and co are doing
- QML-like interface, language independent
- C API

# Things we don't want

- Rendering inside the core library
	- Choose from different rendering backends according to platform
- Ownership of the main loop

# Things that would be nice to have

- Flutter-style hot reloading
- Redux-style time travelling/replays
- An underpinning theoretical foundation for the core concept (like finite state machines used in a specific way)


# A new paradigm that's actually just an old one in disguise: Client-server architecture

Okay so what really is a GUI? it's a user interface that just happens to be rendered. 

## An aside: widget graphs

Why are GUIs traditionally thought of as a widget tree? Because that makes layout and rendering easy. The purpose of a tree is to give an ordering, a hierarchy. If you didn't have the widgets in a tree, you'd have just some bag of widgets each with their own positions - and you can do this perfectly fine, if you specify absolute coordinates for each of the widgets. There are systems that work perfectly fine like this, for example tile-based 2D video games.

Why do we use trees in GUIs? Because we think of GUIs in a hierachical manner: We want text *centered* inside a button. We want the send button *next to* the text input. We want the text input *below* the chat window. 

## #NotAllUIs

Because we think of GUIs like this traditionally, it shapes how we think of the rest of a user interface. But let's forget widget graphs for a minute. 

What does a user interface actually do? It lets users interact with your system. Well, duh, sure. But the key point is that this has no hierarchy: "user interaction" is just a list of things that you can do.

Text interfaces are like this: you have a bunch of keys you can press and the system then does something in response. 

This actually models more accurately what the user is actually doing when they interact with your interface. The user doesn't think "I want to change activities and create a grid of image elements" when they press a button, they think "I want to view my photos, this is the button that lets me view my photos".

User interfaces are simply a list of capabilities, an enumeration of affordances. User interfaces are an API.

# What is a GUI?

Once we are in this mindset, it makes thinking about GUIs and UIs much clearer. To use an API, you have to set some parameters, and then execute one of the available functions.

In a GUI, you have some widgets which control certain pieces of state, and some widgets which correspond to executing functions, and some that do both. 

# A calculator example

Let's say we have an old-school, non-scientific, solar powered calculator (insert image). Calculators like your phone's calculator or a TI-84 have relatively boring interfaces: you type in a string of characters that forms an expression, and then the expression is evaluated. In comparison, old-school calculators have more complicated interfaces (more actions) because they have less complicated state. This topic could be an entirely different blog post about complexity and simplicity in interfaces.

So what actions can we do with our calculator?  Not "We can press a number button, an operation button, or enter", but the actual things that pressing those buttons does. 

Let's start with +. You might say pressing + takes whatever the last number you entered and adds it to whatever the current total is. It actually doesn't do that!

Let's go from the beginning for the following expression `2*3+4=`, so that we should end up with 10 in our display. First we press 2, displaying a 2. Then we press `*`, which appears to do nothing or maybe shows a little highlighted asterisk somewhere on the display. Then we press 3, which changes the display to a 3 (!). Then we press `+`. What happens? We get 6, the result of `2*3`.

Therefore, what pressing an operation button actually does is two things: it applies the *previous* operation and sets the new "previous operation" to be the key we pressed. So what actions do we have and what state do we have? We have the "apply operation" action, which as parameters takes the state "previous operation" (here `*`), "total value" (2), "input value" (3). You can also think of total value and input value as simply "left input and right input". 

Well wait, what about when we pressed `*` the first time, after 2? There was no previous operation to apply, and additionally there wasn't any "previous number" state.



Continue the explanation, but in the end I'm just getting at: UI should have state that it can alter, and operations that it can execute which take only those states. This paradigm extends to all sorts of UI, not just GUIs, but also text UIs, curses UIs, and even things like voice UIs. Layout and rendering are almost afterthoughts.

Buttons shouldn't emit "button pressed" events, they should be directly associated with state mutations and actions (now, this might be achieved via an "onpress" method, but the point is that you associate a user interaction with a widget directly with some sort of action)


