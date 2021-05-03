# Week 2 Exercises
## Operating Systems Intro

1. Most CPUs have two modes that is controlled by a bit in the status register.

    In priviliged (kernel) mode:
    - CPU can execute **all instructions** in its instruction set.
    - CPU has unrestricted access to **memory**.

    In user mode:
    - CPU **control registers** are inaccessible.
    - CPU **management instructions** are inaccessible.
    - CPU only has restricted access to **memory**.
    - Some device **memory and registers** are inaccessible.

    All user programs run in user mode. A user program can obtain services from the operating system using a **system call** to access such restricted resources. 
    
    Having a user-mode offers **protection** by ensuring (possibly malicious) user software do not have unrestricted access to hardware and cause damage.

2. 
    - The OS can act as an **Abstract (Extended) Machine** that abstracts away the hardware and implementation details by providing high level abstractions to make it easier to program with. 
    - The OS can also act as a **Resource Manager** that is responsible for allocating resources between users and processes.

3. 
    - Files fulfil the **Abstract Machine** role by hiding hardware details regarding disks and other IO devices. It presents the programmer with a clean abstract model of **device-independent files**. 
    - Files fulfil the **Resource Manager** role as the OS must manage the **allocation of disk-space**.

4. 
    a. Disable all interrupts - kernel mode
    b. Read time of day clock - user mode
    c. Set time of day clock - kernel mode
    d. Change the memory map - kernel mode
    e. Write to hard disk controller register - kernel mode
    f. Trigger write of all buffered blocks associated with a file back to disk - user mode

## OS System Call Interface

5.  
    a. Child is a **new independent process** that is a **copy of the parent**. ``i`` in the child will have whatever value was in the parent at the point of forking.
    b. ``my_pid`` in a parent is not updated by any action of the child. The parent and child are independent after forking.
    c. The process id of ``/bin/echo`` is whatever the current process id is. ``execl`` replaces the content of the current running process with a specified executable instead of spawning a new process.
    d. From above, ``execl`` essentially ends the current running program so the lines after it won't run if the call is successful.
    e. "Hello World" is printed 4 times if ``FORK_DEPTH`` is 3.
    f. 8 processes are created.

6.
    a. Following code opens or creates ``testfile`` and attempts to write the given ``teststr`` into the file.
    b. A file can also be opened with ``O_RDONLY`` (read mode) or ``O_RDWR`` (read/write) mode.
    c. On success, ``open`` returns the new file descriptor. On failure, -1 is returned.

7. 
    a. The file will be 45 + 5 bytes after two reads.
    b. ``lseek`` is moving the file pointer back, and so the write is overwriting some of the existing text.
    c. ``SEEK_CUR`` which sets the file pointer to the current location plus the given offset and ``SEEK_END`` which sets the file pointer to the end of the file plus the offset.

8.
    a. ``strace`` is tracing the system calls of the given program.
    b. File descriptor 6 is used for the open file.
    c. ``printf`` is a library function that calls ``write`` with file descriptor 1.

9.
    a. This program changes the current working directory and uses ``ls`` to print the contents of that directory.
    b. The current working directory of the shell is the same because the shell forks a child process that runs the code. Each process has its own current working directory, so the change in directory only affects the child process. 
    c. ``/bin/ls`` will run in the parent directory as ``execl`` replaces the content of the child process and inherits the current working directory of the child process.
 
10.
    - ``read()``: is a system call as it is implemented at the kernel level.
    - ``printf()``: is not a system call and instead a library function.
    - ``memcpy()``: is not a system call.
    - ``open()``: is a system call.
    - ``strncopy()``: is not a system call.

## Processes and Threads

11. Three states of a process are **ready**, **running** and **blocked**. Possible causes of process transitions include:
- **Running** to **Ready**:
    - Voluntary ``Yield()``.
    - End of timeslice.
    - Higher priority process becomes ready.
- **Ready** to **Running**:
    - Dispatcher chose the next thread to run.
- **Running** to **Blocked**:
    - Waiting for input:
        - File or network, etc.
    - Waiting for a timer (alarm signal).
    - Waiting for a resource to become available.
- **Blocked** to **Ready**:
    - Resource becomes available.

12. In a N thread uniprocessor: 
    - Running threads = 0 or 1.
    - Blocked = N - Running - Ready.
    - Ready = N - Running - Blocked.

13. In a single threaded system:
    - 1000 / (15 + 1/3 * 75) = 25 requests per second.

    In a multi-threaded system:
    - 1000 / 15 = 66.67 requests per second.
    - Waiting for disk is **overlapped**, so disk operations are not considered.

14. An incorrect result may happen if one thread grabs the current value of ``x``, then another thread grabs the value of ``x`` and increments it and then control is returned to the original thread. This results in only one increment being registered.

15. There is no race condition on ``j`` as it is a local variable. ``i`` however is a global variable and so sections involving ``i`` must be mutually excluded.

16. This function would form a critical region if multiple threads pass in a pointer to a shared global resource.