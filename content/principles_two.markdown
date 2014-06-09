Title: Convolution
Category: Signal Processing
Tags: Principles of Digital Image Synthesis, convolution

So I'm reading the chapter "Signals and Systems" in PDIS, and since I took Professor Goodman's [DSP course](http://www.math.rutgers.edu/courses/357/index.html?arch=Spring_2014) a lot of the material is familiar to me, but presented in a different way or context. It's very neat to see things presented in a slightly unfamiliar way and then realize "oh, I know this." It's somehow validating your knowledge or something and is gratifying in a weird but nice way.

In particular, this sentence really clicked for me in sort of mapping different intuitions to the same underlying idea:
> Convolution is important because it tells us how to use a system's impulse response to find the output of the system to a given input.

(at this point I continued reading)

The exposition in this book is really quite good. Following from the previous statement, we determined that $e^{\omega t}$ is an eigenfunction of LTI systems by taking the convolution with the system's impulse response $h(x)$. (this sounds like a simple statement, or at least a succinct one, but it takes a bit of time to understand) Its eigenvalue is the [frequency response](http://en.wikipedia.org/wiki/Frequency_response) $\int h(\tau)e^{-\omega\tau}d\tau$. 

Then we have:
> This fact reveals that one of the easiest types of functions to study with respect to LTI systems are the complex exponentials, since they pass through such systems unchanged except for complex scaling. If we can represent an input signal as a sum of these functions, then we can find the response of the system to each exponential individually, and then sum the responses together. The Fourier series and transform provide precisely the tools that decompose a signal into a sum of exponentials.

This seems like a very different way to arrive at Fourier series and transform than "let's decompose a function as a sum of sine and cosines because that sounds like fun". Basically, it gives us a reason why we might want to do such a thing a priori.
