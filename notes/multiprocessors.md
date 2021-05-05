# Multiprocessor Systems
## Bus Based Uniform Memory Access
![](https://ars.els-cdn.com/content/image/3-s2.0-B9780121709600500281-f26-01-9780121709600.gif)
- Bus bandwidth becomes bottleneck with multiple CPUs.
- Have a **per-processor cache** to minimise access to memory.

### Cache Consistency
- Usually handled by hardware.
- Writes to one cache **invalidate all other caches**.
    - Also consumes bus bandwidth.

## Operating Systems
### Separate OS For Each CPU
Used in early multiprocessor systems.
- Simple to implement.
- Avoids CPU-based concurrency issues.
- Scales - no shared serial sections.
- Actually used in **modern cloud virtualisation**.

Problems:
- Each processor has **own scheduling queue**:
    - Can have **one processor overloaded** while rest are idle.

- Each processor has **own memory partition**:
    - Can have **one processor thrashing**, and others with free memory.
    - No way to move free memory from one OS to another.

### Symmetric Multiprocessor
Used in modern multiprocessor systems.
- OS **kernel runs on all processors**.
    - Load and resource **balanced between all processors**.
        - Including kernel execution.
- Issue: **Real concurrency** in the kernel.
    - Need to carefully apply synchronisation primitives.

## Synchronisation
### Test and Set
TSL does not work on multiprocessor systems without extra hardware support
- Hardware solution **blocks all other CPUs from accessing the bus** during the TSL instruction to prevent memory accesses by other CPU.
    - Has **mutually exclusive access to memory** for duration of instruction.

Problem: 
- TSL is a busy-wait synchronisation primitive (**spinlock**).
- Lock contention leads to spinning on the lock.
    - Spinning on lock blocks the bus which **slows all other CPUs down**.
        - Independent of whether other CPUs need lock or not.
        - Causes **bus contention**.

### Read Before Test and Set
- Spin reading **cached copy** of lock variable waiting for it to change.
- When it does, use TSL to acquire the lock and **invalidate all cached copies**.
- Greatly **reduces bus traffic**.

### Spinning vs Blocking
Spinning (busy waiting) on a lock makes no sense on a uniprocess.
- No other running process to release the lock.
- Blocking and (eventually) switching to the lock holder is the only sensible option.

Decision is not as clear on SMP systems.
- Lock is held by another running CPU and will be freed **without necessarily switching away** from the requestor.
- Sometimes lock is held for **less time than overhead of switching** to and back, so **spinning is more efficient**.

#### Spinlock Implementation
- Critical sections synchronised via spinlocks are **expected to be short** to avoid other CPUs wasting cycles spinning.
- Spinlock holder **must not be preempted**.
    - Other CPUs will spin until holder is scheduled again.
    - **Interrupts are hence disabled.**