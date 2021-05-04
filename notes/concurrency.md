# Concurrency and Synchronisation
Note: most of the points below are applicable to both **threads AND processes**. For brevity, only threads will be used.

## Overview of the Problem
Situations where a result depends on the order of which threads run are known as a **race condition**.

```c
int count = 0

void increment() {
    int t = count;
    t++;
    count = t;
}

void decrement() {
    int t = count;
    t--;
    count = t;
}
```

Can produce one of -1, 0, 1 depending on exact **execution sequence**. 

Issue arises when a thread uses a **global variable** while a different thread is changing it.

## Critical Regions
### Overview of Critical Regions
**Critical regions** are sections of the program where **shared memory is accessed**. Key to solving concurrency problems is to **ensure no two threads** are in the critical region **at the same time.**

### Requirements for Concurrency Solution
- No two threads may be **simultaneously inside** their critical regions.
- No assumptions made about speeds or number of CPUs.
- No thread running outside its critical region may block any thread.
- No thread should have to wait forever to entire its critical region.

## Potential Mutual Exclusion Solutions
### Lock variable
Enter when ``lock == 0``, wait otherwise.

Problem: consider the following execution sequence on two threads:
```c
while (TRUE) {
                            while (TRUE) {
                                while (lock != 0);
    while (lock != 0);
    lock = 1;
                                lock = 1;
                                critical();
    critical();
    lock = 0;
    non_critical();
                                lock = 0;
                                non_critical();
                            }
}
```

Here, thread 2 sees critical region is available and moves on. But **before setting the lock**, thread 1 runs and also sees critical region is available. Both threads enter the **critical region at the same time**.

Problem arises because the operation of reading the lock is separate to the operation of setting the lock; this is not an **atomic operation**.

### Taking Turns
```c
while (TRUE) {
    while (turn != 0);
    critical_region();
    turn = 1;
    noncritical_region();
}

while (TRUE) {
    while (turn != 1);
    critical_region();
    turn = 0;
    noncritical_region();
}
```

Solution works due to **strict alternation**, but has following problems:
- **Busy waiting**.
- Process must **wait its turn** even while the **other process is doing something else**.
    - With many processes, must **wait for everyone** to have a turn.
        - Does **not guarantee progress** if a process no longer needs a turn.
    - Poor solution when processes require the critical section at **differing rates**.

### Disabling Interrupts
Interrupts can be **disabled before entering** a critical region, and **reenabled after leaving**.

Pros:
- Simple

Cons:
- Only available in **kernel**.
- **Blocks everybody** else, even with no contention.
    - Slows interrupt response time.
- Does not work on **multiple processors**.

### Hardware Support
**Test and set instruction** is used to implement lock variables correct. Ensures process of **reading** and **acquiring** the lock happens in a **single atomic operation**.

Pros:
- Simple
- Available at **user level**.
    - To any number of processors and any number of lock variables.

Cons:
- Busy waits.
    - Consumes CPU.
    - **Starvation** is possible when a process leaves its critical section and more than one process is waiting.

## Overcoming Busy Waiting Problem
### Busy Waiting Problem
**Busy waiting** is when a thread sits in a **tight loop** waiting for **entry into a critical region**. This approach has the problems:
- Wastes CPU time.
- ...

### Sleep/Wakeup Idea
- When process is **waiting** for an event, it calls **sleep to block**.
- The event happens, the event generator (another process) calls wakeup to unlock the sleeping process.
- Waking a ready/running process has no effect.

## Semaphores
### Overview
- If resource not available, corresponding semaphore **blocks any process waiting** for the resource.
- Blocked processes are put into a **process queue** maintained by the semaphore (avoids busy waiting).
- When a process **releases a resource**, it **signals** this by means of the semaphore.
- Signalling **resumes a blocked process** if there is any.
- Wait (P) and Signal (V) operations cannot be interrupted.
- Complex coordination can be implemented by **multiple semapahores**.

### Implementation
```c
typedef struct {
    int count;
    struct process *L;
} semaphore;
```

Assume two simple operations:
- ``sleep`` **suspends** the process that invokves it.
- ``wakup(P)`` **resumes** the execution of a blocked process ``P``.

We now define the **atomic** sempahore operations as such:
```c
wait(S) {
    S.count--;
    if (S.count < 0) {
        // add this process to S.L
        sleep;
    }
}

signal(S) {
    S.count++;
    if (S.count <= 0) {
        // remove a process P from S.L
        wakeup(P);
    }
}
```

## Producer-Consumer (Bounded Buffer) Problem
**Poducer produces data** items and stores the items in a buffer. **Consumer takes the items** out of the buffer and consumes them. 

We must keep current count of items in the buffer and:
- Producer:
    - should sleep when buffer is **full.**
    - wakeup when there is empty space in buffer.
        - Consumer can call wakeup when it **consumes** first entry of full buffer.
- Consumer:
    - should sleep when buffer is **empty**.
    - wakeup when there are items available.
        - Producer can call wakeup when it **adds** the first item to buffer.

### Solving the Producer-Consumer Problem With Semaphores
```c
#define N = 4

sempahore mutex = 1;

semaphore empty = N;

semaphore full = 0;

prod() {                          cons() {
    while (TRUE) {                    while (TRUE) {
        item = produce();                 wait(full);
        wait(empty);                      wait(mutex);
        wait(mutex);                      remove_item();
        insert_item();                    signal(mutex);
        signal(mutex);                    signal(empty);
        signal(full);
    }                                 }
}                                 }
```

## Monitors 
### Overview
- **Higher level** synchronisation primitive.
- **Programming language** construct.
- Idea:
    - Set of procedures and variables are **grouped** in a special kind of module, a **monitor**.
        - Variables only accessed **within the monitor**.
    - One one process/thread can be in the monitor at any one time.
        - Mutual exclusion implemented by **compiler**.

## Condition Variables
### Overview
- Allow **blocking** while waiting for an event (and ensuring mutual exclusion).
    - Typically used inside **monitors**.
        - **Mutex** not needed for the critical region itself since it is **implied by the monitor**.
- Provides **queue** for threads waiting for a resource.
- Thread tests to see if resource is available.
    - If available, use it.
    - Otherwise, add itself to the wait queue.
- When a thread has finished with a resource, it **wakes up** exactly one thread from the queue.
- Does NOT keep track of an **internal counter** like a **semaphore** does.

### Operations
- ``wait``: add calling thread to queue and put it to sleep.
- ``signal``: remove a thread from the queue and wake it up.
    - Under Hansen model: calling process **exits monitor** immediately.
- ``broadcast``: remove and wake-up all threads on the queue.

