# Processes and Threads
1. Ready, Blocked, Running.

Ready -> Running:
- Scheduler picks a ready process to run.

Running -> Ready:
- Process reaches end of timeslice and scheduler runs other process.

Running -> Blocked:
- Process performs blocking system call such as IO.

Blocked -> Ready:
- Process that previously performed IO and blocked now has IO request completed.

2.
**Preemptive multitasking**:
- Rapidly context switching between processes.
- Each process given a **timeslice** to execute.
- Process then gets interrupted by a time which causes it to context switch to another process, which will run until it blocks or until the next tick.

3. 
- Process is an **instance of a program**.
- Has its **own virtual address space** and comprises one or more threads. 
- Process has its own set of file descriptors, VM space, timekeeping data, and some other stuff.

4. 
- Ready queue is a list of threads that aren't currently running but are available to be scheduled next to run.
- There may be several ready queues for each priority level depending on the scheduling algorithm.

5.
- Process **comprises of one or more threads**.
    - Thread must be contained within a single process.
- Thread **inherits the virtual address space** of the parent process, as well as global variables and file descriptors.
- Threads are units of execution within a process.
    - Each thread has a register set, stack, program counter and scheduling attributes.

6. 
- From kernel perspective, each process **only has one thread of execution**.
- To support multiple user-level threads, the process contains code to create, destroy, schedule and syncrhonise user-level threads.
- This **multiplexes many user-level threads** onto the **single kernel thread**, all managed within the process.
- In-process scheduler can run any **scheduling algorithms**, and is independent of kernel's scheduler.
- Needed components for a user-level threads package:
    - TCB: stores information used by the scheduler and queues about a thread.
    - Ready queue: stores threads that are unblocked and are candidates to run next.
    - Blocked queue: stores threads that can't progress until some event occurs.
    - Scheduler: chooses which thread from the ready queue to run next.

7. 
Advantages:
- Thread switching and creation is performed with significantly **less overhead** as it doesn't need to trap to kernel space.
- Can use a scheduling algorithm that is customised for the process.
- Can be implemented on any OS (thread aware or not).
- Can allow for significantly more threads via virtual memory.

Disadvantages:
- The OS is only aware of one kernel thread from the process.
    - => A single user thread that blocks prevents the other user level threads from being scheduled.
    - => **No true parallelism** across different processors.

8. User-level threads are generally **cooperatively scheduled** because they do not have access to the regular timer interrupts as a sufficiently small interval to give the illusion of parallelism.

9. 
Advantages:
- Kernel is **aware of multiple threads** from the application
    - => One blocking thread in an application doesn't prevent other threads in the application from being scheduled.
        - Can **overlap IO with computation.**
    - => True parallelism as threads can be run on different processors.
- Kernel has access to timer interrupts.
    - => **Preemptive scheduling** so a thread cannot monopolise CPU time.

Disadvantages:
- Management of threads at kernel level has **significant overhead** as it requires system calls and hence transition into kernel mode.
- Requires OS support.

10. 
- Thread A running.
- CPU receives timer interrupt.
- Kernel switches to kernel stack for thread A.
- Kernel saves all the relevant registers onto the kernel stack of thread A.
- Scheduler picks next thread to run from its ready queue(s).
- Kernel switches to kernel stack for thread B.
- Kernel loads thread B's registers.
- Warp into thread B.
- Thread B running.

11. ``switchframe_switch()`` in OS161.
- Saves return address (RA), global pointer (GP), local subroutine registers and stack pointer (SP) to the old thread's TCB.
- Restores corresponding registers for new thread.
- Loads SP from new threads TCB.
- Jumps to RA from new thread's TCB.