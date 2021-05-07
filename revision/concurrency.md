# Concurrency
1. A **race condition** is when some result depends on the order of which threads run. An typical example is when multiple threads manipulate the same global variable:

```c
int x = 0;

void f() {
    x += 1;
}
```

2. A **critical region** is a section of code where **shared memory is accessed**. Controlling access by only allowing one thread to be inside a critical section at a time is the key to solving race conditions.

3. 
- **Mutual exclusion**: No two threads may be inside the critical section at the same time.
    - To help prevent race conditions.
- **No assumption** made about speed of the CPU.
    - To create portable solutions that work on different hardware.
- **Progress**: No thread outside its critical region may block any other thread.
- **Bounded**: No thread should have to wait forever to enter its critical region.

4. Turn passing solves the problem but has the following problems:
- Processor must wait its turn even while **other process is doing something else**.
- If different threads use the critical region at **different rates**, performance is limited by most infrequent user.
- If one thread **no longer needs its turns**, the other thread may not progress.

5.
Advantages:
- Easy to implement and efficient.

Disadvantages:
- Only works in **kernel mode**.
- **Blocks all threads** even with no contention.
- **Doesn't work on multiprocessors** as other processors can access resources in parallel.

6. ``test-and-set`` is an **atomic operation** that checks for a lock to be available and acquires it when it is. It prevents race conditions where a thread is preempted between checking the lock and acquiring the lock.

7. The **producer-consumer** problem is a problem that involves filling and depleting a bounded buffer.

Example: **IO buffering**.
- When user process is reading, IO device is producer and process is consumer.
- When user process is writing, IO device is consumer and process is producer.

8. A semaphore is a blocking sychronisation primitive meaning a thread blocks itself when a resource is not available and is woken up by another thread once the resoucre is available.

```c
typedef struct {
    int count;
    struct process *L;
} semaphore;

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

9. A lock can be implemented as a semaphore with count 1.

```c
struct *sempahore lock = create_semaphore(1);
```

10. 
**Monitors**:
- **Programming language construct** where compiler ensures only one thread execute inside a special module called a monitor.
- Other threads are queued and sleeps until the thread inside monitor exists monitor.

**Condition Variables**:
- Entities within monitors to block and wait for events.
- Thread invoking ``wait`` sleeps until another thread wakes it with ``signal``.