Title: Unifying the Types vs Testing debate
Status: draft

after watching a cpp talk about how unit testing mimics the modern scientific method in that we don't try and prove things true, we try and invalidate the null hypothesis (i.e. show the lack of a bug), I realized this is related to the classic "types vs testing" debate.

Per the [Curry-Howard correspondence](https://en.wikipedia.org/wiki/Curry%E2%80%93Howard_correspondence), types are essentially theorems, statements about objects, and the code we write is a "proof" for that theorem (by construction).

Similarly, when we do an experiment (or write a test), really we want to state a theorem about the physical world: "light travels at a certain speed in a vacuum", but we can't prove that theorem, so we are forced to resort to testing that our expectations match reality by doing an experiment, e.g. via [a Fizeau–Foucault apparatus](https://en.wikipedia.org/wiki/Fizeau%E2%80%93Foucault_apparatus).

However, like writing a unit test with specific values, this only tells us about the behavior of the system in this specific, controlled instance.

So the conclusion here is that just like in the real world, we have both proofs and experiments: For things that we can write proofs (types) for, we should, and for everything else we do experiments (tests) to validate our theories.

What this says to me though, is that because computers are mostly mathematical systems, we should strive as much as possible to encode logic into the type system, because proofs are stronger than experiments.
