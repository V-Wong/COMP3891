# Virtual Memory
## Overview
- Give each process illusion of a **private view** of the whole address space.
- Create illusion of a very **large main memory** by storing recently unused memory in **secondary storage**.

## Paging
- Partition physical memory into small equal sized chunks called **frames**.
- Divide each process's virtual (logical) address space into same size chunks called **pages**.
    - Virtual memory address consists of a **page number and offset** within the page.
- OS maintains a **page table**.
    - Contains the frame location for each page.
    - Used by hardware to translate each virtual address to physical address.
    - Relation between virtual address and physical memory addresses given by page table.
- Process's physical memory does **not have to be contiguous**.

## On-Demand Paging
Only parts of the program image need to be resident in memory for execution.
- Transfer presently **unused pages to disk**.

## Page Fault
Referencing an invalid page triggers a page fault. Two broad categories include:
- Illegal address:
    - Signal or kill the process.
- Page not resident:
    - Get an empty frame.
    - Load page from disk.
    - Update page table.
    - Restart faulting instruction.

## Thrashing
- Higher degree of multiprogramming means **less memory available per process**.
- Some process's working sets may **no longer fit in RAM**.
    - **Increasing page fault rate**.
- Eventually many processes have insufficient memory.
    - Can't always find a runnable process.
    - Decreasing CPU utilisation.
    - System become IO/limited

Thrashing greatly decreases performance and is usually recovered by:
- In the presence of increasing page fault frequency and decreasing CPU utilisation:
    - **Suspend a few processes** to reduce degree of multiprogramming.
    - Resident pages of suspended processes will migrate to backing store.
    - More physical memory becomes available.
    - Resume suspended processses alter when memory pressure erases.


## Page Table
Page table is logically an **array of frame numbers indexed by page number**.

### Page Table Entry
|Attribute|Description|
|-|-|
|**Valid Bit**|Indicates a valid mapping for the page.|
|**Modified Bit**|Indicates the page may have been modified in memory. Also called dirty bit.|
|**Reference bit**|Indicates the bit has been accessed.|
|**Protection Bits**|Read/write/execute etc.|
|**Caching Bit**|Indicates processor should bypass the cache when accessing memory.|

### Two Level Page Table
Page tables **grow with address space** which can be massive even if only a small portion is used at a time.

![](http://web.cs.ucla.edu/classes/spring13/cs111/scribe/15b/2-level_page_table.jpg)
- Second level **does not need to be allocated** if not used.
- Substantially **saves space** if only a small portion of memory is used.
- Generalises to three level, four level, etc....

### Inverted Page Table
**Inverted page table** contains **one entry per frame** in real memory and is **indexed by frame number**. 

**Hash anchor table** keyed by hash of the page number is used to generate possible indexes in the page table. The algorithm to convert from a virtual address is as follows:
- Compute hash of page number.
- Extract index from hash table.
- Use this index into inverted page table.
- Match the PID and page number in the IPT entry.
- If match:
    - use the index value as frame number for translation.
- Else:
    - Get next candidate IPT entry from chain field (**internal chaining**).
    - If null chain entry => page fault.

Advantages:
- Grows with size of RAM and not virtual address space.
    - Saves a lot of space.

### Hashed Page Table
Similar to a page table but store **frame number as separate field** in the table. 

Intermediate **hash anchor table** is removed and we **hash directly into the page table**.

Advantages:
- Grows with size of RAM, not virtual address space.
- Have **multiple entries map to the same physical page frame**.
    - Allows for **different processes** to **share the same physical frames**. 

Drawbacks:    
- Table can fill up depending on the **level of sharing**.

## Replacement Policies
Different policies decide which page to throw out when physical memory is used up and a new page needs to be allocated.

### Optimal Replacement Policy
- Toss the page that won't be used for the **longest time**.
- **Impossible to implement** (requires predicting the future perfectly).
- Useful as a **theoretic reference point**.

### FIFO Replacement Policy
- Toss out the **oldest** page.
- Easy to implement.
- Problematic as the age of a page isn't necessarily related to usage.
- An old page might actually be used quite frequently.

### Least Recently Used
- Toss the **least recently used** page.
- Assumes that page that has **not been referenced for a long time** is **unlikely to be rerferenced** in the near future.
- Will work if locality holds.
- Difficult to implement efficiently as we need a **timestamp to be kept for each page** and **updated on every reference**.

### Clock Page Replacement (Second Chance)
- Employs a **usage or reference bit** in the frame table.
- Set to one when page is used.
- While scanning for a victim, reset all the reference bits.
- Toss the first page with a **zero reference bit**.

## Memory Management Unit
Hardware on the CPU responsible for **converting virtual addresses to physical addresses**.

### Translation Lookaside Buffer
TLB is a **cache** which holds a (recently used) subset of page table entries. 

Exploits **principal of locality** to greatly reduce the average number of physical memory references per virtual reference.