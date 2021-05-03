# Processes and Threads
We often require an operating system to be able to:
- **Interleave execution of several processes** to maximise processor utilisation while providing reasonable repsonse time.
- Allocate resources to processes.
- Support **interprocess communication** and **user creation of processes**.

## Overview of Process Model
### Processes
- Also called "task" or "job".
- Execution of an **individual program**.
- **Owner of resources** allocated for program execution.
- Encompasses one or more **threads**.

### Threads
- **Unit of execution**.
- Can be traced
    - List the sequence of instructions that execute.
- Belongs to a process
    - Executes within it.

### Multiprogramming
- One physical program counter switches between processes.
- Conceptual model of multiple **independent, sequential processes** (with a single thread each).
- **Only one** program active at any instant on CPU (pseudoparallelism).

## Implementation of Processes
A processes' information is stored in a **process control block** (PCB). PCBs together form a **process table**.

### Example Process Table Entry Fields
|**Process Management**|**Memory Management**|**File Management**|
|--|--|--|
|Registers|Pointer to text segment|Root directory|
|Program counter|Pointer to data segment|Working directory|
|Program status word|Pointer to stack segment|File descriptors|
|Stack pointer||File descriptors|
|Process state||User ID|
|Priority||Group ID|
|Scheduling parameters|||
|Process ID|||
|Parent process|||
|Process group|||
|Signals|||
|Time when process started|||
|CPU time used|||
|Children's CPU time|||
|Time of next alarm|||

## Lifecycle of a Process
### Process Creation Causes
- **System initialisation**:
    - Foreground processes (interactive programs).
    - Background processes.
        - Email server, web server, print server, etc.
        - Called a daemon (Unix) or service (Windows).
- Execeution of a process creation system **by a running process**.
    - New login shell for an incoming SSH connection.
- **Users request** to create a new process.
- Initiation of a **batch job**.

### Process Termination Conditions
- Normal exit (voluntary).
- Error exit (voluntary).
- Fatal error (involuntary).
- Killed by another process (involuntary).

### Process/Thread States
- Running (actually using CPU at that instant)
- Blocked (unable to run until some external event happens)
- Ready (runnable; temporarily stopped to let another process run)

### Events That Cause Process Transitions
- _Ready_ to _Running_:
    - All other processes have ran enough (scheduler decides to pick this process to run).
- _Running_ to _Ready_:
    - Voluntary ``Yield()``.
    - End of timeslice (scheduler decides running process has run long enough).
- _Running_ to _Blocked_:
    - Waiting for input:
        - File or network, etc.
    - Waiting for a timer (alarm signal).
    - Waiting for a resource to become available.
- _Blocked_ to _Ready_:
    - Resource on which process was originally waiting on becomes available.

## Scheduler
Scheduler decides which of the _Ready_ **processes to run**. There are various **algorithms** for scheduling.

### Two Queue Algorithm
- Queue for **ready** events and for **blocked** ev-ents.
- **Avoids scanning** list of processes to select one to **make ready**. 

    ![](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQM0pJoyFwNIPisKTOrHGrslOqFC_wEczvxxg&usqp=CAU)

### Multi Queue Algorithm
- Having one blocked queue is inefficient as one resource being blocked has **no effect on another resource**. 
- Use a (shorter) blocked queue for **each resource**.
    
    ![](https://teaching.csse.uwa.edu.au/units/CITS2002/lectures/lecture08/images/f3.08b.png)

## Thread Model
### Thread vs Process
|Per process items|Per thread items|
|-|-|
|Address space|Program counter|
|Global variables|Registers|
|Open files|Stack (local variables)|
|Child processes|State|
|Pending alarms||
|Signals and signal handlers||
|Accounting information||

### Thread Usage
|Model|Characteristics|
|-|-|
|Threads|Parallelism, blocking system calls|
|Single-threaded process|No parallelism, blocking system calls|
|Finite-state machine|Parallelism, nonblocking system calls, interrupts|

### Why Threads?
- **Simpler to program** than state machine.
- **Less resources** than a complete process:
    - Cheaper to create and destroy.
    - Share resources (especially memory) between them.
- Performance: Threads waiting for I/O can be **overlapped with computing threads**.
    - Note: if all threads are compute bound, then no performance improvement on a uniprocessor.
- Threads can take advantage of **parallelism** available on machines with **multiple processors**.