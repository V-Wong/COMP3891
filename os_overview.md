# Operating Systems Overview

## Role of an Operating System
An operating is a software layer on top of hardware that manages all parts of the system. It controls all computer resources and provides the base upon which application programs can be written. 

The following points are additional views of the OS.

### Abstract (or Extended) Machine
- **Extends basic hardware** with added functionality.
- Provides high-level **abstractions**.
    - Easier to program with.
    - Common core for all applications.
- **Hides hardware and implementation details**.
    - More portable code.

### Resource Manager
- Responsible for **allocating resources** to users and processes.
- Must ensure:
    - No starvation (process is not able to acquire desired resource to progress its execution)
    - Allocation of resources according to some policy.
    - System is overall efficient.

## Structure of an Operating System
### Privileged Component
#### Kernel
- Portion of operating system running in **privileged mode**.
- Usually **resident in memory** while computer is running.
- Contains fundamental functionality:
    - Whatever is required to implement other services.
    - Whatever is required to provide security.
- Contains most-frequently used functions.

#### Operating System is Privileged
- Applications should not be able to interfere or bypass the OS.
    - OS can enforced the "extended machine".
    - OS can enforce resource allocation policies.
    - OS can prevent applications from interfering with each other.

## Interaction Between Application Programs and the OS
- The OS runs in **Kernel Mode** while application programs run in **User Mode**.
- The OS interacts via load and store instructions to all memory, CPU and device registers.
- Applications interact with themselves and via functions call to library procedures.
- Applications can **interact with the OS** via a **system call** to request a service. E.g. accessing a hard disk drive.

### Note on System Libraries
Systems libraries are libraries of support functions (procedures, subroutines).
    - A subset of library functions are system calls
        - ``strcmp(), memcpy()`` are pure library functions.
            - They only manipulate memory within the application or perform computations.
        - ``open(), close(), read(), write()`` are system calls.
            - They cross user-kernel boundary.
            - Implementation mainly focused on passing request to OS and returning result to application.

### Aside: Privilege-less OS
- Some **Embedded OSs** have no privileged component.
    - E.g. PalmOS, Mac OS 9, RTEMS.
    - These OSs can implement standard OS functionality, but cannot enforce it.
        - All software runs together.
        - No isolation.
        - One fault potentially brings down entire system.