# Scheduler Activations
1. Hybrid multithreading allows true thread-level parallelism as the kernel can run the kernel-level threads on different CPUs.

2. If M > N and N user level blocks for IO, then the remaining M - N user level threads can't do anything even if they are not doing IO. I.E. can't necessarily overlap IO with processing.

3. An **upcall** involves the kernel returning to user-space in a fixed pre-defined area of memory. This allows the kernel-level scheduler to **notify the user-level scheduler** of scheduling events, allowing the user-level scheduler to choose **what action to take**. 

4.
Improvement over kernel level threads:
- Fewer kernel stacks - kernel only stores number of activations and stacks for blocked activations.
- Fast user-level thread switching.

Improvements over user level thread:
- Threads that block in the kernel can be switched with another user-level thread, improving performance with IO-bound process.
- Can take advantage of multiple processors.

5.
- User-level thread A performs IO-related system call.
- Thread A blocks in kernel.
- Kernel scheduler upcalls the user-level scheduler, notifying that thread A is blocked.
- User-level scheduler runs a different user-level thread, thread B.
- Thread A's IO request completes.
- Kernel scheduler upcalls the user-level scheduler, notifying that thread A is unblocked.
- User-level scheduler chooses whether to run thread A or continue with thread B.

6.
- **New**: new activation becomes available for process to use.
- **Preempted**: process have one less activation available for use.
- **Blocked**: user level thread associated with the process has become blocked. Process can choose another user level thread to run instead.
- **Unblocked**: user level thread associated with process has become unblocked. Process must choose whether to continue running the current process or to run the unblocked process.