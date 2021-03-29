# Week 5 Tutorial Problems
## Memory Hierarchy and Caching
1. Types of memory in memory heirarchy:
    - Registers
    - Cache
    - Main memory
    - Magnetic disk
    - Magnetic tape

    The **capacity** increases down the heirarchy but so does the **access time**. Usually a computer will have a **small amount of very fast memory** and a **large amount of slower memory**.

    Furthermore, data is accessed less frequently towards the bottom of the heirarchy. This phenomenon is known as **locality of access** where most accesses are to a **small subset** of all data.

2. Disks can stream data quite fast but only under the assumption that the data is already **under the head**. If the header is not above the correct data, time is lost to **seeking** and **rotational latency** which are in the magnitude of milliseconds.

3. The faster processor with less cache is better suited towards small applications. The slower processor with more cache is suited towards running larger applications. Ultimately, it depends if an application is **CPU constrained** or **memory constrained**.

## Files and File Systems
4. Disk operations for various block allocation methods.
- **Contiguous allocation:**
    - Added to beginning: 100 reads, 101 write.
        - All elements shifted right.
    - Added in middle: 50 reads, 51 writes.
        - Half the elements shifted right
    - Added at end: 0 reads, 1 write.
        - Assumed space at the end.
    - Removed from beginning: 0 reads, 0 writes.
        - Simply update starting block in file control block. 
    - Removed from middle: 49 reads, 49 writes.
        - Shift everything left.
    - Removed from end: 0 reads, 0 writes.
        - Simply update file size in file control block.

- **Linked allocation:**
    - Added to beginning: 0 reads, 1 write.
        - Simply write first block then update file control block.
    - Added in middle: 50 reads, 2 writes.
        - Traverse to correct file block, write link to new block position, then write new block.
    - Added at end: 100 reads, 2 writes.
        - Traverse to last file block, write link to new block position, then write new block.
    - Removed from beginning: 1 read, 0 writes.
        - Find position of second file block, then update starting block in file control block.
    - Removed from middle: 50 reads, 1 write.
        - Traverse to the correct file block, rewrite link to the next next file block.
    - Removed from end: 99 reads, 1 write.
        - Traverse to second last file block, remove link to the last node.

- **Single level indexed allocation:**
    - Added to beginning: 0 reads, 1 write.
    - Added in middle: 0 reads, 1 write.
    - Added at end: 0 reads, 1 write.
    - Removed from beginning: 0 reads, 0 write.
    - Removed from middle: 0 reads, 0 writes.
    - Removed from end: 0 reads, 0 writes.

    - For all of these, we are simply updating the file control block in memory, so very few accesses to the disk are required.

5. Storing 400 bytes in a 512 byte block is **internal fragmentation**.

6. Writing to directories can cause damage to the **directory** and in the worst case bring the entire file system into an **unstable state**.

7. Linked-list and i-node are good approaches for block allocation as the **size can vary** widely. Contiguous allocation **must allocate the maximum** possible size of the file, which will waste a lot of space when the file is significantly smaller than the maximum.

    If **random access** is required, then linked lists are not suitable as they **don't provide constant time random access**.

8. The virtual file system provides an **interface (or contract)** between the system's kernel and a more concrete file system. It is an **abstraction layer** that allows the client to access **different types** of concrete file systems in a **uniform way**.

9. Larger blocks require **less FS metadata** while smaller blocks **waste less disk space** from internal fragmentation. 

    For sequential access, larger block size will lead to **fewer I/O operations** and **more contiguous disk accesses**.

    For random access, larger block size will lead to more **unrelated data** being loaded.

10. The alternative would involving **passing the filename** into ``read()`` or ``write()`` along with an offset. The file is then opened for each ``read()`` or ``write()`` operation. This is obviously much more expensive than keeping the file open.

11. A rename syscall would just change the string stored in the **directory entry**. A copy operation will require **much more I/O** as each block of the original file is **copied into a newly allocated block** in the new file. Additionally, the original file blocks must be deallocated.

12. Not being able to move the file pointer means random access will either:
    - Be extremely **expensive** as one would have to **read sequentially** from the start each time until the appropriate offset is arrved at OR
    - Require an **extra argument** that would need to be added to ``read()`` and ``write()`` to specify the offset before performing the respective operation.