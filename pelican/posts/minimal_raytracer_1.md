Title: Ray-tracing in 50 lines
Date: 2018-07-02
Category: Raytracing
Tags: Raytracing, Rust, Geometry
Slug: raytracing-minimal-1
Author: Harry Stern
Summary: TODO
Status: Draft

# What is Raytracing?

Ray-tracing is a method of generating images from 3D scenes by approximately simulating light directly, rather than using texture-mapped triangle rasterization as in real-time 3D systems like OpenGL, Direct3D, and Vulkan. This blog post aims to do the very least amount of simulation possible to be called a "ray-tracer". At some point in the future I would like to do an equivalent for triangle rasterization, which is actually somewhat more complicated in the minimal case.

# Raytracing Basics

In our minimal example, we have the following situation:

- There is a "camera" which acts as a [pinhole camera](https://en.wikipedia.org/wiki/Pinhole_camera), located at a given position, that points in a direction.
	- The camera "projects" an image onto a screen, which in the human eye and in a real camera projects onto a screen behind the camera, but for our purposes will act more like a movie projector and project onto a screen in front of the camera. There are images later.
- The screen has a given number of pixels, which are square for simplicity. In "screen-space", the pixels start at the top-left corner and increase downwards to the given height, and to the right to the given width. We say that `width/height` is the aspect ratio of our screen.
- There is a single sphere in our scene, given by a position and a radius.

TODO insert image here

# The Camera

If the image were projected behind the screen, as in a traditional pinhole camera or the human eye, the image would actually be inverted and the math would be a bit more tricky.
