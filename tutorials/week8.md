# Week 8 Tutorial Problems
## Memory Management
1. 
    - **Internal** fragmentation occurs when a process does not use all the **allocated memory in its region**. This leads to space wasted **internal** to the allocated memory region.

    - **External** fragmentation occurs when there is **sufficient memory** to allocate for a process, but the memory is arranged **non-contigously**. This leads to space wasted as the memory is not useable for **contiguous allocation**.
 
2. In **fixed (static) partitioning**, the regions of memory given to processes are fixed (of potentially different size) and setup at boot time. This is simple to implement but has **poor memory utilisation due to internal fragmentation**. The OS has to pick the best partition for a given process and **cannot resize regions** to accomodate for processes with memory usage that doesn't match the partition sizes.

3. Base and limit registers are special hardware that maps each **processs's addresss space** onto **different parts of physical memory**. When a process is run, the base register is loaded with the physical address where the program begins in memory and the limit register is loaded with the length of the program. Every time a process references memory, the CPU hardware automatically **adds the base value** before sending the address out on the memory bus. Simultaneously it checks whether the **address is within the limit range**, otherwise the access is aborted.

    Using base and limit registers give each process its own **private address space**. Additionally most implementations protect the base and limit registers such that **only the operating system** can modify them.

    Problems with this approach include:
        - Need for an **addition** to be performed on **every memory reference**. 
        - Physical memory allocation **must still be contiguous** and requires a **whole process to be in memory** at once. 
        - Does not support **partial sharing** of address spaces (libraries or multiple instances of the same code).

4. Binding program addresses to physical memory:
    - **Compile/link time:** Compiler binds the addresses. It requires the **run location** to be known at **compile time**. This forces a **recompile** to be needed if the run location **changes**.
    - **Load time:** Compiler generates **relocatable** code. Loader binds the addresses at **load time** (copied into memory). This process slows loading (**increases startup latency**).
    - **Run-time:** Logical compile-time addresses translated to physical addresses by special hardware. Most flexible but incurs the **cost of translation** on every memory reference.

5. Algorithms for allocating regions of contiguous memory:
    - Note: we maintain a linked list of **available free memory ranges**. Each node contains the base address and the size of the range. This list is kept in order of **increasing addresses** to simplify **merging of adjacent holes**. The list nodes themselves can be **stored in the holes themselves** which means overall no net usage of space.

    - First-fit algorithm:
        - Scan the list for the first entry that fits:
            - If greater in size, break it into an allocated and free part.
        - Aims to **find a match quickly** and hence **minimise amount of searching**.
        - Biases allocation to one end of memory.
        - Tends to preserve larger blocks at the end of memory.

    - Next-fit algorithm:
        - Like first-fit, but begins search from the point in the list where the **last request suceeded**.
        - Aims to **spread allocation more uniformly** over entire memory to avoid skipping over small holes at start of memory.
        - Performs **worse** than first-fit as it **breaks up the large free space** at end of memory.

    - Best-fit algorithm:
        - Chooses the block that is **closest in size** to the request.
        - Performs **worse** than first fit:
            - Has to **search complete list**.
            - Since smallest block is chosen for a processs, the smallest amount of external fragmentation is left which creates **lots of unusable holes**.

    - Worst-fit algorithm:
        - Chooses the block that is **largest in size** with the aim of leaving a usable fragment left over.
        - Poor performer:
            - Has to **search complete list**.
            - Does not result is significantly less fragmentation.

6. **Compaction** shuffles memory contents to place all **free memory together** in one large block. The aim is to **reduce external fragmentation**.

## Virtual Memory
7. **Swapping** is where a process is brought into main memory in its **entirety**, run for a while, and the put completely back on disk.

    Swapping allows the OS to **run more programs** than what would fit in memory if all programs remained resident in memory.

    Swapping is **slow** as it has to copy the entire program's in-memory image out to disk and back.

8. **Paging** is the technique of **splitting the virtual address space** into fix-sized units called **pages**. The corresponding units in the physical memory are then called **page frames**. Memory is transferred **to and from disk** in **units of pages**.

9. All virtual memory system have page sizes a power of 2 because the **lower bits** of a virtual address are **not translated** and passed through the MMU to form a physical address.

10. A **Translation Lookaside Buffer** is special hardware usually inside the MMU that consists of a **small number of mappings** between virtual page number and physical page number (along with other metadata). It acts as a **cache** that prevents needing to constantly reference memory multiple times for a given address.

11. In a **two level** page-table, virtual addresses are split into three parts. In a 32 bit address this is typically:
    - 10 bits for indexing into the top level page table.
    - 10 bits for indexing into the second level page table.
    - 12 bit offset within a page.

    This gives 2^10 * 2^10 = 2^20 total pages of 2^12 bits (4KB) each. The aim of a multi-level page table is to **save memory**. While there are up to 2^20 pages, not all of the second level tables are necessarily in memory at a given time. Amount of memory needed for a page table is now **not dependent on size of the address space** but instead dependent on **memory actually used by the process**. I.E. **lazy allocation**.

12. 
    - 100% miss ratio: 3 accesses. One for accessing first level page table. One for accessing second level page table. One to access actual address.
    - 95% hit ratio: 0.95 * 1 + 0.05 * 3 = 1.1 accesses.

13. A **page fault** is a trap that occurs when an **invalid page** is referenced. There are two broad categories of page fault types:
    - **Illegal address**: process is killed.
    - **Page not resident in memory**: 
        - Get an empty frame.
        - Load page from disk.
        - Update page table.
        - Restart the faulting instruction.

14. Recall the contents of a TLB entry:
    - Key field:
        - **Virtual page number**: program address with lower 12 bits cut off, since the low-order bits don't participate in the translation process.
        - **Address space identifier**: magic number unique to each task's distinct address space.

    - Data field:
        - **Physical frame number**: physical address with lower 12 bits cut off. In address translation, VPN bits are replaced with corresponding PFN bits to form true physical address.
        - **Cache control bit**: set 1 to make page uncacheable.
        - **Write control bit**: set 1 to allow stores to this page to happen.
        - **Valid bit**: set 0 to make this entry usable.
        - **Global bit**: set to disable the ASIC-matching scheme.

    Recall translation of address:
        - CPU generates virtual address.
        - Lower 12 bits of virtual address separated off, and the resulting VPN together with the current value of the ASID field in ``EntryHi`` used as the key to the TLB.
        - Consult valid and write bits.

    - Translation exercise.
        - (0x00028123 & PAGE_FRAME) | 0x00000200 -> 0x28200.
            - Corresponding data field: 0x0063f400.
            - 0x0063f400 = 0b000000000110001111110**1**0000000000.
            - Valid bit set to 1 => Invalid entry.

        - (0x0008a7eb & PAGE_FRAME) | 0x00000200 -> 0x8a200
            - No correponding data field (ASID mismatch).

        - (0x0005cfff & PAGE_FRAME) | 0x00000200 -> 0x5c200
            - Should have no matching entry?

        - (0x0001c642 & PAGE_FRAME) | 0x00000200 -> 0x1c200
            - Corresponding data field: 0x00a97600.
            - 0x00a97600 = 0b1010100101110**110**00000000.
            - Not global, is valid, is writeable.
            - Physical address: 0x00a97642.

        -  (0x0005b888 & PAGE_FRAME) | 0x00000200 -> 0x5b200
            - Corresponding data field: 0x002af200.
            - 0x002af200 = 0b10101011110**010**00000000.
            - Not global, is valid, not writeable.
            - Physical address: 0x002af888.

        - (0x00034000 & PAGE_FRAME) | 0x00000200 -> 0x34200
            - Corresponding data field: 0x001fc600.
            - 0x001fc600 = 0b1111111000**110**00000000.
            - Not global, is valid, is writeable.
            - Physical address: 0x001fc000.

15. An **inverted page table** contains **one entry per frame** in real memory and is **indexed by frame number**. A **hash anchor table** keyed by a hash of the page number is used to generate possible indexes in the page table. The algorithm to convert from a virtual address is as follows:
    - Compute hash of page number.
    - Extract index from hash table.
    - Use this index into inverted page table.
    - Match the PID and page number in the IPT entry.
    - If match:
        - use the index value as frame number for translation.
    - Else:
        - Get next candidate IPT entry from chain field (**internal chaining**).
        - If null chain entry => page fault.

16. A **hashed page table** is similar to a page table but instead of the frame number being used as an index, we store it as a separate field in the table. The intermediate **hash anchor table** is removed and we hash directly into the page table. The main advantage of this approach is that we can have **multiple entries map to the same physical page frame**. This allows for **different processes** to **share the same physical frames**. The drawback of this is that the table can fill up depending on the **level of sharing**.

17. For large virtual adress spaces that are sparsely populated, inverted and hashed page tables are preferable as their size depends only on the size of physical memory and not on the virtual address space.

18. 
    - **Temporal locality**: states that **recently accessed items** are **likely to be accessed in the near future**.
    - **Spatial locality**: states that **items whose addresses are near one another** tend to be **referenced closed together in time**.