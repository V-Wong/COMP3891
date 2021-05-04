# Implementation of Processes and Threads
## Processes
### Process Modes
Processes can run in two modes:
- **User mode**:
    - Processes scheduled by the kernel.
    - **Isolated** from each other.
    - **No concurrency issues** between each other.
- System-calls transition into and return from the kernel.
- **Kernel mode**:
    - Nearly all activities still associated with a process.
    - Each process has a separate **in-kernel stack**.
    - Kernel memory **shared** between all processes.
    - **Concurrency issues** exist between processes concurrently executing in a system call.

## Threads
### User-level Threads
- User level TCB, ready queue, blocked queue and dispatcher.
- **Kernel has no knowledge** of the threads (only sees a single process).
- If a thread blocks waiting for a resource held by another thread inside the same process, its state is saved the dispatcher switches to another ready thread.
- Thread management are implemented in a **runtime support library**.

Pros:
- Much **faster** than kernel level:
    - No need to trap (take syscall exception) into kernel and back.
- Dispatcher can be **tuned to application** (with priorities).
- Can be implemented on **any OS** (thread or non-thread aware).
- Can easily support **massive numbers of threads** on a per-application basis.
    - Use normal application **virtual memory**.

Cons:
- Threads have to **yield manually** (no timer interrupt delivery to user level).
    - Poorly designed/implemented thread can **monopolise CPU time** (cooperative multithreading).
- Does not take advantage of **multiple CPUs**.
- If a thread makes a blocking system call, the process (and **all internal threads**) blocks
    - Can't overlap IO with computation.

### Kernel-level Threads
- TCB stored in kernel.
- Thread management calls implemented as **system calls**.

Pros:
- **Preemptive** multithreading.
- Parallelism:
    - Can overlap blocking IO with computation.
    - Can take advantage of **multiprocessor**.

Cons:
- Requires **kernel entry and exit** which is expensive.

## Context Switching
### Overview
A context switch refers to:
- A switch between threads:
    - Saves and restores state associated with a thread.
- A switch between processes:
    - Involves above, plus extra process specific state.

### Occurence
Can happen any time OS is invoked:
- On a **syscall**.
    - Mandatory if system call blocks or on ``exit``.
- On an **exception**.
    - Mandatory is offender is killed.
- On an **interrupt**.
    - Triggering a dispatch is the main purpose of the **timer interrupt**.

A thread switch can happen **between any two instructions**.

### Implementation
- Process/thread must not notice that a context switch has occured.
    - OS must save all state that affects the thread.
        - State also called process/thread **context**.

Steps of a context switch:
1. Point stack pointer to kernel stack (originally at user stack).
2. Trapframe pushed on stack.
    - Contains user-level program counter, stack pointer and relevant registers.
3. Call C code to process syscall, exception, or interrupt.
    - Results in C activation stack building up.
4. Kernel decides to perform a context switch:
    - Chooses a target thread (or process).
    - Pushes kernel context onto the process kernel-stack.

    - Any other existing thread must:
        - Be in kernel mode.
        - Have a similar stack layout to the stack we are currently using.

    - Save th current stack pointer in the PCB (or TCB), and load the stack pointer of the target thread.
        - Context has now been switched.
