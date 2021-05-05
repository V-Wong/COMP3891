# Scheduler
## Overview
Schedule is responsible for deciding which ready process to **run next**.

## IO Bound + CPU Bound
IO-bound process:
- Spends most of its time **waiting for IO** to complete.
    - Small bursts of CPU to process IO and request next IO.

CPU-bound process:
- Spends most of its time **computing**.
- Time to completion largely determined by received CPU time.

We need a mix of CPU-bound and IO-bound processes to **keep both** CPU and IO systems **busy**.

Processes can go from CPU to IO bound (or vice versa) in different **phases of execution**.

### Improving Responsiveness
- Running IO-bound process delays CPU-bound process by very little.
- Running CPU-bound process prior to an IO bound process delays the next IO request significantly.
    - **No overlap** of IO waiting with computation.
    - Results in device not as busy as possible.
- Favour **IO-bound processes over CPU-bound processes**.

## When Is Scheduling Performed
- A new process.
    - Run the parent or the child.
- A process exits.
    - Who runs next?
- A process waits for IO.
    - Who runs next?
- A process blocks on a lock.
    - Who runs next? The lock holder?
- An IO interrupt occurs.
    - Who do we resume, the interrupted process or the process that was waiting?
- On a timer interrupt.

## Goals of Scheduling Algorithms
- **Fairness**:
    - Give each process a fair share of the CPU.
- **Policy enforcement**:
    - What ever policy chosen, the scheduler should ensure it is carried out.
- **Balance/Efficiency**:
    - Try to keep all parts of the system busy.

## Round Robin Scheduling
Round Robin scheduling is used in **interactive scheduling**.

- Each process is given a **timeslice** to run in.
- When the timeslice expires, the next process preempts the current process, and runs for its timeslice, and so on.
    - Preempted process is placed at end of queue.
- Implemented with:
    - A ready queue.
    - A regular timer interrupt.

Pros:
- Fair, easy to implement.
Cons:
- Assumes all processes are equal.

### Timeslice Considerations
Too short:
- Waste a lot of **time switching** between processes.

Too long:
- System is **not responsive**.

## Priority-Based Scheduling
- Each process (or thread) is associated with a **priority**.
- Provides basic mechanism to **influence scheduler decision**.
    - Scheduler will **always pick higher priority**.
- Priorities can be defined internally or externally.
    - Internal: IO bound or CPU bound.
    - External: importance to user.
- Implemented with **multiple queues** for each priority, each having its own round robin.

## Unix Scheduler
![](https://d3i71xaburhd42.cloudfront.net/91b878f6e61cfb0e5e4241308b378284ac5b670e/15-Figure10-8-1.png)

Two-level scheduler:
- High-level scheduler schedules processes between **memory and disk**.
- Low-level scheduler is **CPU scheduler**.
    - Based on multi-level queue structure with round robin at each level.

### Priority Recalculations
Highest priority is scheduled.
- Priorities are **recalculated** once per second, and reinserted in appropriate queue.
    - Avoid starvation of low priority threads.
    - Penalise CPU-bound threads.


Priority = CPU_usage + nice + base (lower is higher priority).
- CPU_usage = number of clock ticks.
    - A process that spends a **lot of CPU time** is **penalised**.
    - This **decays over time** so that CPU bound background jobs **do not suffer starvation**.
- Base is a set of hardwired, negative values used to **boost priority** of **IO bound** system activities.

## Multiprocessor Scheduling
### Single Shared Ready Queue
Pros:
- Simple.
- Automatic load balancing.

Cons:
- **Lock contention** on ready queue can be a major bottleneck.
    - Due to frequent scheduling or many CPUs or both.
- Not all CPUs are equal.
    - Last CPU a process ran on is likely to have more related entries in the cache.

### Affinity Scheduling
Affinity scheduling tries to run a process on the CPU it ran on last time.

### Mutliple Queue SMP Scheduling.
- Each CPU has its own ready queue.
- Coarse-grained algorithm assigns processes to CPUs.
    - Defines their affinity, and roughly balances the load.
- Bottom-level fine-grained scheduler:
    - Is the frequently invoked scheduler (on blocking on IO, a lock, or exhausting a timeslice).
    - Runs on each CPU and selects from its own ready queue.
        - Ensures affinity.
    - If nothing is available from the local ready queue, it runs a process from another CPU's ready queue rather than go ideal.
        - Work stealing.

Pros:
- No lock contention on per-CPU ready queues in the common case.
- Load balancing to avoid idle queues.
- Automatic affinity to a single CPU for more cache friendly behaviour.