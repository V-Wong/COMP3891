# Week 3 Exercises
## Synchronisation Problems
1. A **mutex (binary semaphore)** can be used such that the other thread B blocks thread A from accessing the variable until it has completed updating the variable.

2. **Semaphores** can be used to allow only 10 threads to access the room at any one time, while forcing all additional threads to wait for a thread to exit. We can define a semaphore as follows:

```c
typedef struct {
    int count;
    struct process *L;
} semaphore;

/* Assume two operations:
    - sleep(): suspends process/thread that invokves it.
    - wakeup(P): resumes execution of blocked process P.
*/ 

void wait(S) {
    S.count--;
    if (S.count < 0) {
        // add process to S.L
        sleep(); 
    }
}

void signal(S) {
    S.count++;
    if (S.count <= 0) {
        // remove a process P from S.L
        wakekup(P);
    }
}
```

We can then use the semaphore as follows:

```c
static semaphore s = create_semaphore(10);

void f() {
    wait(s);
    enter_room();
    signal(s);
}
```

3. We can use a **semaphore** approach to this problem.
```c
waiters_count = 0;
disk_block_status = NOT_READY;
block_mutex = create_semaphore(1);
block_sem = create_semaphore(0);

wait_block() {
    P(block_mutex);
    if (disk_block_status == READY) {
        V(block_sem);
    } else {
        waiters_count++;
    }
    V(block_mutex);
    P(block_sem);

    // use resource
}

make_block_ready() {
    P(block_mutex);
    disk_block_status = READY;
    while (waiters_count != 0) {
        waiters_count--;
        V(block_sem);
    }
    V(block_mutex);
}
```

4. We can fix deadlocks as follows:

```c
void me() {
    P(mutex);
    /* do something */

    P(data);
    /* do something else */

    V(mutex);

    /* clean up */
    V(data);
}
 
void you() {
    P(mutex)
    P(data);

    /* do something */

    V(data);
    V(mutex);
}
```

The alternating order of resource acquisition is what causes the deadlock. We hence modify the functions to always attempt to acquire ``mutex`` before ``data``.

5. The following sequence creates a deadlock:
```c
lock *file1, *file2, *mutex;

void laurel() {                         void hardy() {
    lock_acquire(mutex);
    // do something
    lock_acquire(file1);
    // write to file 1
    lock_acquire(file2);
    // write to file 2
    lock_release(file1);
    lock_release(mutex);
    // do something
                                            // do something
                                            lock_acquire(file1);
                                            // read from file 1

    // can't acquire file1                  // can't acquire file 2                  
}                                       }
```

We can prevent deadlocks by changing the order of resource acquisition as follows:

```c
void laurel() {
    lock_acquire(mutex);
    /* do something */
	
    lock_acquire(file1);
    /* write to file 1 */
    lock_release(file1);
 
    lock_acquire(file2);
    /* write to file 2 */
    lock_release(file2);

    /* do something */

    lock_acquire(file1);
    /* read from file 1 */
    lock_release(file1);

    lock_release(mutex);
}
 
void hardy() {
    /* do stuff */

    lock_acquire(file1);
    /* read from file 1 */

    lock_acquire(file2);
    /* write to file 2 */

    lock_release(file1);
    lock_release(file2);

    lock_acquire(mutex);
    /* do something */
    lock_acquire(file1);
    /* write to file 1 */
    lock_release(file1);
    lock_release(mutex);
}
```

6. Synchronised linked list
```c
static struct lock *list_lock;
static struct list_t *list;

void init(list_t *) {
    // initialise lock
    // initialise list
}

void add_head(list_t *list, node_t *node) {
    lock_acquire(list_lock);
    // add head to list
    lock_release(list_lock);
}

void add_tail(list_t *list, node_t *node) {
    lock_acquire(list_lock);
    // add tail to list
    lock_release(list_lock);
}

struct node *remove_head(list_t *list) {
    lock_acquire(list_lock);
    // remove head from list
    lock_release(list_lock);

    return old_head;
}

struct node *remove_tail(list_t *list) {
    lock_acquire(list_lock);
    // remove tail from list
    lock_release(list_lock);

    return old_tail;
}

void insert_after(node_t *in_list, node_t *new_node) {
    lock_acquire(list_lock);
    // insert new_node after in_list
    lock_release(list_lock);
}

void insert_before(node_t *in_list, node_t *new_node) {
    lock_acquire(list_lock);
    // insert new_node before in_list
    lock_release(list_lock);
}

remove(node_t *in_list) {
    lock_acquire(list_lock);
    // remove in_list
    lock_release(list_lock);
}
```

This will not deadlock as no thread can hold a lock while waiting for another lock. Once a thread holds the lock and enters the critical section, it must be able to leave the critical section since it does not have to wait for any other lock. The next thread waiting then gets access to the lock and so on.

The thread subsystem in OS/161 is not synchronised as the code is written under the assumption that the **code runs mutually exlusively**. This is ensured by **disabling interrupts** on the uniprocessor.

7.  a. This is a deadlock as no progression can be made without at least one diner dropping their fork.
    b. This is starvation. While the fork repeatedbly becomes free, it is always allocated to a younger person and so the older person never gets to use the fork.
    c. This is a livelock as the state of the forks constantly change, but no progress is being made in eating the dinner.

8. Starvation is when high priority keep executing and **low priority processes get blocked for indefinite time**.

9. This is a livelock as the state of the resource is constantly changing but neither process is making progress. Both ``seek`` and ``read`` should be considered a part of the same critical region. So a lock should be used as follows:

```c
lock_acquire(disk_lock);
seek();
read();
// other stuff necessary
lock_release(disk_lock);
```

10. We have 4 conditions for deadlocks and possible solutions as follows:
    a. M**utual exclusion condition**: each resource assigned to one process or is available.
    - Allow multiple processes to access a resource at the same time. Clearly not viable.

    b. **Hold and wait condition**: thread holds resource while waiting for another.
    - Require process to request resources before starting, hence a process never needs to wait for what it needs. Problematic as it is not always possible to know what resources are needed at the start of a run. It also ties up resources another process could be using.

    c. **No preemptive condition**: resource cannot be forcibly taken from process.
    - Forcibly take away a resource from a process. This is problematic as a process often needs the resource to function correctly.

    d. **Circular wait condition**: circular chain of 2 or more resources. Each is waiting for resource next in the chain.
    - Order resources to prevent circular dependencies. May be difficult but is the most viable option.

11.  a. Still needs:

    |r1|r2|r3|r4|
    |--|--|--|--|
    |0|0|0|0|
    |0|7|5|0|
    |6|6|2|2|
    |2|0|0|2|
    |0|3|2|0|

    b. The system is in a safe state as there exists a scheduling order such that the system won't deadlock: p1 (already done), p4, p5, p2, p3.

    c. The system is not deadlocked currently as we can still make progress with resource assignment.

    d. There are no processes that become deadlocked.

e.
- The request cannot be safely granted immediately.
- The system will eventually be unsafe.
- After the sequence p1, p4, p5: p2 and p3 may become deadklocked.

12. The strategy is to use a **lock per fork**. To avoid deadlock, we always acquire the lower numbered fork first, including the wraparound case.
```c
struct lock *fork_locks[NUM_PHILOSOPHERS];

void take_both_forks(unsigned long phil_num)
{
    int low, high;

    low = phil_num;
    high = (phil_num + 1) % NUM_PHILOSOPHERS;

    if (low > high) {
        low = high;
        high = phil_num;
    }

    lock_acquire(fork_locks[low]);
    lock_acquire(fork_locks[high]);
}


void release_forks(unsigned long phil_num)
{
    lock_release(fork_locks[phil_num]);
    lock_release(fork_locks[(phil_num + 1) % NUM_PHILOSOPHERS])
}
```