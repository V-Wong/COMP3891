# Week 4 Exercises
## R3000 and assembly
1. On MIPS architecture, jump and branch instructions have a delay slot where the **instruction after the jump and branch** instruction is **executed before the jump and branch** is executed.
    - Caused by **instruction pipelining** which involves dividing instructions into sequential steps with different parts of **instructions processed in parallel** by different processor units. 

2. a. ``arg1`` returns its return value in ``v0``.
b. ``arg2`` does not need to refer to the stack because its two arguments can be entirely stored within the 4 **argument registers**. In addition, there are **no local variables**, so no space on the stack is needed to allocate them.
c. ``jr ra`` jumps the to address stored in ``ra``. This register is usually **set during a function call** to the next instruction. This will hence jump back to the caller and start executing the next instruction of the original function.
d. ``a0`` contains the first argument to the function.
e. The ``move`` instruction is after the ``jal`` instruction in ``arg1`` because of the **branch delay** causing the ``move`` to execute before the ``jal``.
f. ``arg5`` and ``arg6`` need to reference the stack because it cannot store all its arguments in the 4 **argument registers**, so arguments 4, 5, 6 are hence **stored on the stack**.

3.
```mips
004000f0 <reverse_print>:
    <!-- Allocates 24 bytes on the stack -->
    4000f0:       27bdffe8        addiu   sp,sp,-24 
    <!-- Stores return address on stack -->
    4000f4:       afbf0014        sw      ra,20(sp)
    <!-- Stores local variable (argument) on stack -->
    4000f8:       afb00010        sw      s0,16(sp)

    <!-- Loads value of memory into v0 -->
    4000fc:       80820000        lb      v0,0(a0)
    400100:       00000000        nop

    <!-- if v0 == 0: jump to 400124 -->
    400104:       10400007        beqz    v0,400124 <reverse_print+0x34>    
    
    <!-- else -->
    <!-- Move argument into s0 and recursively call self -->
    400108:       00808021        move    s0,a0
    40010c:       0c10003c        jal     4000f0 <reverse_print>
    400110:       24840001        addiu   a0,a0,1 # this is executed before previous instruction

    <!-- Perform write -->
    400114:       24040001        li      a0,1
    400118:       02002821        move    a1,s0
    40011c:       0c1000af        jal     4002bc <write>
    400120:       24060001        li      a2,1
    
    <!-- Restore return address -->
    400124:       8fbf0014        lw      ra,20(sp)
    <!-- Restore previously stored argument from previous recursive call -->
    400128:       8fb00010        lw      s0,16(sp)

    <!-- Return from function call and unallocate stack -->
    40012c:       03e00008        jr      ra
    400130:       27bd0018        addiu   sp,sp,24
```

4. Recursion requires constantly **storing and retreiving values on the stack** which is dangerous as the kernel stack is small and overflows will crash the entire system.

## Threads
5. Both models allow threads to voluntarily give control back. However they differ as follows:

|Pre-emptive multithreading|Cooperative Multithreading|
|-|-|
|Scheduling algorithm picks a process and lets it run for a maximum of some fixed time. If still running at end of time interval, it is supsended and **scheduler picks another process to run**.|Scheduling algorithm picks a process to run and **lets it run until it blocks** or voluntarily releases the CPU.|
|Prevents a poorly designed/implemented thread from monopolising CPU time|Poorly designed/imeplemented thread can use up entire CPU time|
|Has overhead when context switching between threads|No overhead from context switching.|

6. **User-level threads** implement the thread control blocks, ready queue, blocked queue, and dispatcher at the **user level**. The **kernel has no knowledge of these threads** and only sees a **single process**. If a thread blocks waiting for a resource held by another thread inside the same process, its state is saved and the dispatcher switches another ready thread.

User-level threads advantages:
- User-level thread switching is much **faster than kernel level**.
- Dispatcher can be tuned specifically to the application.
- Can be implemented on any OS.
- Can easily support massive numbers of threads on a per-application basis.

User-level threads disadvantage:
- Have to ``yield()`` manually as there is no **timer interrupt delivery** at the user level. 
- Is usually a form of **cooperative multhreading** where a single thread can consume the entire CPU time.
- Does not take advantage of **multiple CPUs**.
- If a thread makes a blocking system call, the entire process (and all internal threads) blocks. 
    - Cannot block individual threads.
    - Cannot overlap I/O with computation.

**Kernel-level threads** implement threads at the **kernel level**. This includes thread control blocks, the ready queue, blocked queue and scheduler. Thread management calls are then implemented as **system calls**.

Kernel-level threads advantages:
- **Preemptive multithreading** where threads cannot monopolise the entire CPU time.
- Allows for parallelism.
    - Can overlap block I/O with computation.
    - Can take advantage of multiprocessor.

Kernel-level threads diadvantages:
- Thread creation, destruction, blocking and unblocking requires kernel entry and exit.
    - More expensive than user-level equivalent.

7. The web server is likely using **kernel-level threads**. If it were to use user-level threads, then reading from the file will **block all other threads**. This server hence **can't do anything else** like respond to other client requests in the meantime. Using kernel-level threads will eliminate this problem as **only individual threads will block** while reading from the file, allowing others to still work.

8. ``switch_thread(cur_tcb, dst_tcb)``:
    - The function **saves the registers** required to **preserve the compiler calling convenetion** (and registers to return to the caller) onto the **current stack**.
    - The function saves the **resulting stack pointer** into the current TCB, and sets the SP to the SP stored in the destination TCB.
    - The function then **restores the registers** that were stored previously on the destination (now current) stack, and returns to the destination thread to continue where is left off.

## Kernel Entry and Exit
9. The **exception program counter (EPC)** register contains the **address of the instruction** that was running **when an exception occurred**. When the exception handler completes, the EPC register allows the program that was interrupted to be **resumed**. This servers the same purpose as ``$ra`` for regular subprograms but for exceptions.

10. Bits 0 to 5 in the status register create a three level stack for **exception infomation**. The most recent exception information is stored in bits 0 and 1. When a new exception occurs, this information is pushed to bits 2 and 3, and the new exception information stored in bits 0 and 1. This process continues up to bit 5 to allow storing of information of the **3 most recent exceptions**. The previous exception information can be restored with ``rfe``.

11. The ``ExcCode`` in the ``Cause`` register will be set to **8** when a system call exception occurs.

12. Kernel programmers must be careful when implementing system calls as it **bridges the gap** between **userland applications** and the **priviliged kernel**. Careful attention must be made so that **malicious data from the userland** do not take control or break the kernel (and by extension the system as a whole).

13. a. The 'C' function calling convention must always appear to be adhered to after any syscall wrapper function completes. This involves **saving and restoring preserved registers**. The system call convention also uses the calling convention of the C-compiler to **pass arguments to OS/161**. Having the same convention as the compiler means the system call wrapper can **avoid moving arguments** around as the compiler has already placed them where the OS expects to find them.
    b. The OS/161 kernel code does the saving and restoring of preserved registers. The syscall wrapper function does very little.
    c. At minimum, the wrapper function must add the **system call number** to the arguments passed to the wrapper function. It's usually added by setting an agreed-to register to the value of the system call number.s

14. It is not required for the library function and the system call to have the same name. In fact, system calls do not really have names at all. All exceptions are just index numbers in a jump table (C switch statement). The name of the library function is important to the end user as it is what appears in their program.

15. It is usually not important for a programmer to know which library function results in a system call outside of very **high performance situations** where the **kernel transition is expensive** relative to the overall program.

16. Activities when timer interrupt resulting in context switch:

    |Who|What|
    |-|-|
    |Timer device|Raise interrupt line|
    |CPU|Generates an interrupt exception|
    |CPU|Switches from user to kernel mode|
    |CPU|Begins executing the **Kernel Interrupt Handler (KIH)**|
    |KIH|Changes the SP to the kernel stack for the interrupted process|
    |KIH|Saves the user registers for the interrupted process onto the stack|
    |KIH|Determines the source of the interrupt to be the timer device|
    |KIH|Calls the **Timer Interrupt Handler (TIH)**|
    |TIH|Acknowledges the interrupt to the timer device|
    |TIH|Calls the Scheduler|
    |Scheduler|Chooses a new process to run|
    |Scheduler|Calls the Kernel to switch to the new process|
    |Kernel|Saves the current process's in-kernel context to the stack|
    |Kernel|Switches to the new process's kernel stack by changing SP|
    |Kernel|Reads the new process's in-kernel context of the stack|
    |Kernel|Restores the user registers from the stack|
    |Kernel|Sets the processors back to user mode|
    Kernel|Jumps to the new user process's PC|