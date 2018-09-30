Title: Random thoughts on testing and the TDD book by Kent Beck
Author: Harry Stern
Status: Draft
Date: 1970-01-01
Category: Software development
Tags: testing, TDD, mutation testing, mocking, property testing

# Notes on Test Driven Development by Kent Beck

# Mocks

This section is mostly a response or agreement with [this blog post ](https://martinfowler.com/articles/mocksArentStubs.html) by Martin Fowler.

## Outside-in vs bottom-up

The difference between these two is not the end result: you can end up with working, tested code either way like this. The difference is in how easy it is for the programmer to do so. With bottom-up, writing unit tests firsts and very few mocks, you always have working code, and can easily, for example, revert to the previous commit and be in a working state. If you write the acceptance/system/etc tests first, you will not have working code for a while and instead continue to pile up failing tests, or, if you use mocks, you simply build a tower of mocks that do nothing. 

---

# type systems

There's lots of talk about the relationship between strong type systems and strong testing procedures (see [here](http://blog.cleancoder.com/uncle-bob/2016/05/01/TypeWars.html) and [here](https://www.facebook.com/notes/kent-beck/functional-tdd-a-clash-of-cultures/472392329460303), and [here]() for some examples)

as with the difference between writing unit tests first vs writing system tests first (outside-in vs bottom-up) the difference is not in the end result but the view from a programmer's perspective.

the power of strong type systems lies in the ability to reason locally about the code. If you have a function in rust, you can always know what type a variable is, and what operations it can perform. Certainly with dynamic languages you can do some level of static analysis and have IDE plugins that let you see what a variable *might* be, but in highly dynamic languages you never really know without actually executing the program.



---
# Mutation testing and property testing

mutation testing: fix test inputs, change output
property testing: change test input, fix "output"

in the red-green-refactor cycle, property testing adds confidence to the "green" part - that your code is working
mutation testing adds confidence to the "red" part - that your tests are working! 
