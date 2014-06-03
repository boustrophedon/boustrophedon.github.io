Title: CPU caches and GPU shared memory
Tags: Hardware, caches, GPU, CUDA
Date: 2018-10-15
Status: Draft

I was watching [a Scott Meyers talk on CPU caches](https://www.youtube.com/watch?v=WDIkqP4JbkE) and towards the very end I realized something: Managing per-block shared memory is simply manually managing a "L4" CPU cache. Linear memory access patterns are [coalesced](https://cvw.cac.cornell.edu/gpu/coalesced) such that it mimics the effect of linearly traversing data in a cache line (and in fact, Meyers mentions that strided memory access is detected by modern CPUs and this is also the case for coalesced memory access), but at the end he also fielded a question about whether we can "pin cache lines", and the answer being kind of but you really don't want to.

However, in GPU programming, this is effectively what shared memory is: in a given thread block, you perform a main memory access, load it into a cache, and keep it there for a given duration specifically to reduce latency when accessing that same information again. In fact, [there are functions](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__DEVICE.html#group__CUDART__DEVICE_1g6c9cc78ca80490386cf593b4baa35a15) that allow you to dynamically partition the size of the L1 cache and available shared memory for some (older, it seems) GPUs.  

In fact, the CUDA best practices guide [specifically says](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#shared-memory-in-matrix-multiplication-c-ab) "This illustrates the use of the shared memory as a user-managed cache when the hardware L1 cache eviction policy does not match up well with the needs of the application or when L1 cache is not used for reads from global memory."
