Title: Ray tracing and property testing, part 1: Background
Date: 2018-07-02
Category: Ray tracing
Tags: Ray tracing, Rust, Geometry
Slug: ray-tracing-minimal-1
Author: Harry Stern
Summary: TODO
Status: Draft

If you don't want to read the math background, skip to [the code on GitHub]() or [Part 2, ]()

# What is ray tracing?

[Ray tracing](https://en.wikipedia.org/wiki/Ray_tracing_(graphics)) is a general term for a method of generating images from 3D scenes by approximately simulating the path light takes through a scene. Alternatives to ray tracing include methods like triangle rasterization, commonly used in real-time 3D systems like OpenGL, or scanline algorithms like Reyes, which were used in commercial renderers for movies and TV for a long time.

There are a million blog posts about "I made a ray tracer :)", so my focus in these posts are simplifying the coordinate transforms and intersection tests with easy vector math, and how to test a ray tracer/graphics code using property testing. This series aims to do the very least amount of simulation possible to be called a ray tracer.

# What is property-based testing?

You're probably better off just reading the descriptions from the property testing frameworks themselves, like [QuickCheck for Haskell](http://hackage.haskell.org/package/QuickCheck), [Hypothesis for Python](https://hypothesis.works/), or the one we'll be using, [Proptest for Rust](https://github.com/AltSysrq/proptest). In particular, there's a [very good explanation](https://hypothesis.works/articles/what-is-property-based-testing/) by the author of Hypothesis.

You can think of property-testing as type-based fuzzing on steroids, but it's something a bit more. The basic idea is that instead of writing a specific, static test, where both the inputs and outputs are specified as constants, we test that given a class of inputs, the output satisfies a given property. As an example, code fuzzers like [afl](https://en.wikipedia.org/wiki/American_fuzzy_lop_(fuzzer)) can be thought of as simple property testers that test the property "does the program crash", but they generally have more sophisticated test-generation methods than property testing frameworks.

Property testing frameworks allow us to easily write detailed, unit-test-level property tests, without using a generic code fuzzer. In particular, it's easy to combine different input generators to make new ones, and it takes care of doing much of the actual case generation for you. Proptest also has nice features like saving the failure case inputs to disk, and doing shrinking on failure cases to find simpler examples.

As an example, a traditional unit test for integer addition might be: "Given the inputs 2 and 2, assert that the output is 4.". This is a good, important test to have! It's a very basic sanity test. However, even ten or a hundred of these tests don't give that much confidence that the code is correct: the implementation could be a precomputed table or even an interpolation polynomial!

If we instead test the properties of the code, we get both a wider range of inputs and much more fine-grained detail when something goes wrong. As an example, for addition we might want to test the properties $a+0 = 0 + a = a$, $a+b = b+a$, $a+(b+c) = (a+b)+c$, and "if $a>0$ and $b>0$ then $a+b>0$".

This is more of an aside, but the last property is interesting because it asserts that given some other property ($a,b > 0$), another property holds. We can write a generator to make inputs with a given property when testing another property, essentially building a tree or perhaps DAG of properties of our code. This could probably be a separate blog post, but it would be neat if a framework kept track of the dependencies in your proptests explicitly, so that you could trace up the tree to see the lowest-level property that is violated when something goes wrong.

## Things property testing doesn't help with

- Hard-to-generate edge cases (e.g. `abs(MIN_INT)`)
- Performance tests (though in theory if your framework lets you fix a seed value for the rng, you could use it)
- End-to-end/acceptance tests

Overall, property testing is a great way to codify assumptions and increase confidence in your code. Property testing most useful in unit and integration tests, because each individual test needs to be able to run quickly.

# Property testing with ray tracing

Graphics code is somewhat notorious for being hard to test - who hasn't written a bunch of OpenGL code and run it only to see a completely black window. Getting the first triangle to appear is always the hardest part!

The fact that libraries like OpenGL and Direct3D are essentially IO libraries are part of the reason why it's hard to test graphics code, but in contrast the basic code for a hand-rolled raytracer is relatively easy to test. Of course, for both cases it's easy enough to write end-to-end tests that simply compare the resulting image to a gold master, but gold master tests are more like regression tests than anything else.

What you'd actually like to test to gain confidence in your code are *properties* like "are my primary rays pointing in the direction I expect them to?", "is a triangle that is in front of the camera being rendered?", "is the lighting smooth?", "does global illumination work?", or even better "does the ceiling of a Cornell box recieve enough light?". These are all great candidates for property tests!

# Ray tracing Basics

In our tiny ray tracer, we have the following set up:

- There is a camera which acts as a [pinhole camera](https://en.wikipedia.org/wiki/Pinhole_camera), defined by its position in world space, the direction it's pointing, and its up vector.
	- The camera projects an image onto a screen a given distance away from the camera, which in the human eye and in a real camera is behind the viewing aperture, but for our purposes will act more like a movie projector and project onto a screen in front of the camera.
	- For simplicity, the field of view (fov) is at the "mathematical default" of 90 degrees. The field of view is essentially just a scaling operation on the screen - it just changes the area we can see by making the screen bigger. If we were to add a fov, we would simply multiply each sample coordinate by $\tan(\texttt{fov}/2)$. It is easy to derive this from a diagram.
- The output is a rectangular array of pixels, whose dimensions are an input parameter. In image-space, the pixels start at the top-left corner and increase downwards to the given height, and to the right to the given width. We say that $\frac{width}{height}$ is the aspect ratio of our image.
- We compute the samples for our images by transforming the image coordinates into world coordinates, and cast rays from the camera through the computed coordinates. The value of the sample at the given image coordinate is the color of the pixel at that coordinate.
- There is a single sphere in our scene, given by a position and a radius.
- There are no light sources in our scene. Of course, this means we're not really rendering an image, it's more of a hit-buffer - did the ray hit an object. In later posts we will add a light and code to do lighting.

![A picture showing a camera casting rays through pixels in the screen, hitting a sphere, with other rays from a light source casting a shadow on the ground.](https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Ray_trace_diagram.svg/640px-Ray_trace_diagram.svg.png "Original image from https://en.wikipedia.org/wiki/File:Ray_trace_diagram.svg")

# Spaces

Lots of introductions to ray tracing talk about a bunch of different spaces: world space, camera space, object space, normalized device coordinates, etc. and use matrices to perform transformations between these spaces. In real-time raster-based systems, this is a necessity, and production ray tracers also use similar matrix-based transforms because it's generally faster. For educational purposes it's nice to write everything out with vectors, so that is what we do in the code as well. 

In terms of the order in which we do transformations, ray tracing and rasterization work almost exactly oppositely. Ray tracing starts at the pixels and then goes through the camera and into world space. Rasterization-based pipelines work "backwards": each object is described in object coordinates, and is transformed through camera space, world space, perspective-transformed space (which actually transforms the objects *from* a frustum *into* a rectangular space), and into pixel/device coordinates. 

For this ray tracer, all our inputs and outputs are either in pixel space or world space, but internally we also transform from pixel space to screen space, and the camera also defines a coordinate system that is used when transforming from screen space to world space.

We start with pixel coordinates which range from 0 to `width-1` in the x axis and 0 to `height-1` in the y axis.

We then transform into screen space. The purpose of screen space is to transform the pixel samples into evenly-spaced coordinates centered around (0,0). It ranges from $\pm\frac{\texttt{aspect}}{2}$ in the x axis and $\pm 0.5$ in the y axis, so that we have a rectangle with the width equal to the aspect ratio and the height equal to 1.

The next space that we have to deal with is "camera space", but we actually transform samples from screen space directly to world space. The camera is defined in terms of world space and we use it in the transformation, but we don't explicitly transform into camera space itself, where the camera is at the origin.

Finally, we have world space, which is just a standard 3D cartesian coordinate system.

## An aside: pixels aren't little squares

["A Pixel Is Not A Little Square"](http://alvyray.com/Memos/CG/Microsoft/6_pixel.pdf) is the title of a famous memo by [Alvy Ray Smith](https://en.wikipedia.org/wiki/Alvy_Ray_Smith) about how (who would have expected) pixels are not little squares. I'm mentioning this because I called the inital space that we start in "image or pixel space", but it's only partially accurate to call it that.

The core of the memo (but it is very short and worth reading) is that a pixel is simply a sample at a point. If we want to then display the image over some area, we do some sort of filtering, transforming, and rescaling to reconstruct the image - the simplest of which is a box filter (little squares!). The concept is probably easier to understand when you have less "little squares" experience and intuition - the scanner and printer examples in the memo are good, and if you're familiar with audio sampling then this is exactly the same problem.

From a ray tracing perspective, consider that if you want to render an image with given dimensions, and you shoot a single ray for each of the samples, the samples you take (i.e. the rays you cast) will be spaced out with some distance between them. One way you might try to increase the accuracy of your image is to shoot more rays from some of the points in between your "main" sample points. What do you do with these extra samples? You could simply display them, and increase the resolution of your image. If you don't want to do that, you have to combine them together in some way to get the original number of samples you wanted - this is a reconstruction filter! Now, imagine doing the same operation but solely with your original number of samples, and break your mind from the prison of little squares.

In the end, for this ray tracer we're basically using little squares though. 

# Math

We aren't using a math library, just `[f32;3]` arrays of floats, for both vectors and points. We implement a few simple functions on them: 

## Addition and subtraction
These are straightforward coordinate-wise addition and subtraction.

## Scale
This is again a straightforward coordinate-wise scale operation.

## The dot product

![A diagram showing a vector projection](https://upload.wikimedia.org/wikipedia/commons/7/72/Scalarproduct.gif "Original image from wikipedia https://commons.wikimedia.org/wiki/File:Scalarproduct.gif")

The [dot product](https://en.wikipedia.org/wiki/Dot_product) is a fundamental operation on vectors of any dimension. For two three-dimensional vectors $u, v$, we compute it as $u_1 \cdot v_1 + u_2 \cdot v_2 + u_3 \cdot v_3$ i.e. we multiply each element of the vectors coordinate-wise and take the sum. Because it is also equal to $|a||b|\cos(\theta)$, it has a variety of uses geometrically since it relates the coordinates of the vectors to the angle between them.

We use it in two ways. First, to test whether a vector is pointing in the same direction as another: If vector A were the normal of a plane, is vector B pointing to the same side of the plane as A, on the plane, or the other side of the plane? Second, as a projection operator: A vector with length $a \cdot b$ and direction $a$ gives the projection of $b$ in the direction of $a$.

## The cross product

![A diagram showing the cross product and the area of a parallelogram formed by the vectors](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Cross_product_parallelogram.svg/720px-Cross_product_parallelogram.svg.png "Original image from wikipedia https://en.wikipedia.org/wiki/File:Cross_product_parallelogram.svg")

The [cross product](https://en.wikipedia.org/wiki/Cross_product) is an interesting operation because unlike the dot product, it's relatively simple in 3D but gets much more complicated in higher dimensions. Geometrically, the cross product of two vectors gives you a third vector that is orthogonal to the first two. Its magnitude is equal to the signed area of the parallelogram formed by the first two vectors, which can be computed as $|a||b|\sin(\theta)$.

We use it to determine the third axis of the camera coordinate system given the forward and up directions.

# The Camera

The camera is defined as a struct containing its position, the direction it is pointing, the up direction, and the near plane (also called the focal plane) which here is simply the distance from the camera to the screen we are projecting through. This is the simplest possible camera description: we're not including even basic features like field of view as mentioned above, and we're not including even simple fancy effects like depth of field.

## Why do we need the up vector?

Why do we need to specify the up direction? Because if you look at something, what you see depends not only on the direction you're looking but also how your head is tilted. If you imagine an axis pointing from your neck through the top of your head, perpendicular to your eyes, this is the "up" vector. 

This only defines two axes however, so what about the third? The third is entirely determined by the handedness of your coordinate system.

## Coordinate system handedness
Handedness is a property of a coordinate system given an ordering of the axes and/or a chosen direction that represents forward.

You have to worry about this in OpenGL and Direct3D because normalized deviced coordinates are a pre-defined coordinate space with a given handedness, whereas we get to choose all the spaces. The choice we make here is whether to take cross(up, forward) or cross(forward, up) to get the third axis. In the end it doesn't really matter.

# Image space

![A cool drawing with a grid superimposed representing image space]({static}/images/image_space.png)

Right off the bat I have to mention again that these squares are not pixels, and the drawing shows a rectangular grid only for illustration purposes. Pixels are not little squares. Image space as mentioned above is a rectangular space ranging from 0 to `width-1` and 0 to `height-1`. Each point in image space is a pair $(x,y)$ of two integer coordinates, representing *a sample* taken. In our case, a pixel represents a single ray cast and so a single sample, but in more advanced renderers there's usually some sort of multisampling happening for antialiasing, and advanced camera models may bend light or integrate multiple casts, and so on.

Image space is the output space of our code: we take the value of the sample at each point in image space and put it into an image.

# Screen space

![A cool drawing with a grid superimposed representing screen space]({static}/images/screen_space.png)

Screen space is just image space with different coordinates. We use screen space to make it easier to transform sample positions from 2D to 3D. We could directly plug in the formula from our image to screen space function into the ray generation function, but it's nicer to think about it using screen space as an intermediary.

Image coordinates are integer-indexed, but screen space coordinates are floating-point values. 

## The myth of pixel centers

Often you will see in ray tracing tutorials that the $+0.5$ term in the formula for turning pixel coordinates into screen space is "to sample at the center of a pixel." Well, as we know, pixels aren't little squares. But the formula works - if you leave the term out the image is not centered in the screen. This gives a pretty big clue as to what we're doing: centering the samples in the space, so that they're symmetric around (0,0). 

The reason why people think this is necessary again comes from real-time raster-based graphics systems: in fragment shaders in OpenGL the `gl_FragCoord` variable ["assumes pixel centers are located at half-pixel centers"](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/gl_FragCoord.xhtml) (I'm not sure if one of the instances of "centers" should be replaced with "coordinates"), but in DirectX [this is not the case (?)](https://aras-p.info/blog/2016/04/08/solving-dx9-half-pixel-offset/). This means you will have to offset by half a pixel-length when doing texturing, for example. (I think, I could be getting this part wrong).

# Camera space

---


# Property testing the ray generation function

Note that if we return "0,0,0" from the ray generation function, the direction test passes but the length test fails. If we pass "0,0,0" the direction test fails (because the dot product becomes 0, which means the rays are pointing in the same direction. we could handle this in our test because our generated rays should never be pointing in the "up" or "right" directions)

---

testing increases the confidence we have that our code is correct
property testing is basically a multiplier on our confidence in our code

the tdd cycle of red-green-refactor increases the confidence we have that our *tests* are correct: going from red to green lets us make sure our tests are working
mutation testing is then a multiplier on our confidence in our tests
 
using both property testing and mutation testing should then act even more multiplicitavely?

---

future work:

in the same way we check that the ray-hits are contiguous (locally check for neighbors), if we were generating normals we could check that the normals are locally smooth - this is essentially a way to test that the shading "looks smooth" (of course you should also test that the shading is calculated properly from the normals - i'm not sure that this isn't subjective though and would be better served via gold master testing)


---

bugs that property testing help me find:

- I forgot to add 0.5  to the x and y coordinates.
- make clear the constraints on forward and up vectors: they have to be nonzero and orthogonal (and therefore not collinear, or equal)
- I wasn't multiplying the forward vector by the nearplane distance when computing the ray coordinates

bugs that property testing wouldn't help you find:
corner cases
should\_panic tests
	- eg if you had a fancier Screen struct with a new method, you would probably want it to return a Result with an error or panic if you pass in 0,0

---

Property testing builds a DAG, and this is how it is different from fuzzing. (In this post)[https://hypothesis.works/articles/what-is-property-based-testing/] by the author of Hypothesis, a property testing framework for Python that inspired proptest, he goes back and forth on whether property testing is fuzzing.

Property testing should build a directed acyclic graph with "does it crash" at the root. It's not a tree because you can form diamonds - given property A and property B, you can test "given property A *and* property B, we have property C."

---

