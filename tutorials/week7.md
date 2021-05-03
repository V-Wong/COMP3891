# Week 6 Tutorial Problems
## Files and File Systems
1. Linux (EXT2) preallocates 8 blocks on a write to a file as a potential ***performance optimisation**. It allows for **better contiguity** when there are sequential writes while **minimising external fragmentation**. Unused preallocated blocks are released when the file is closed so that space is not wasted.

2. Linux (EXT2) uses a **buffer cache** in RAM so that files changes aren't necessarily immediately written to disk. This can be a problematic as an OS crash or power failure can cause **loss of data** or even leave the filesystem in an **inconsistent state**. **Write-through cache** can be used as an alternative where modified blocks are written immediately to disk. This gives much **better consistency** are the cost of **lowered performance**. 

3. A directory is simply a **file** that **maps file names to inode numbers**. It does not contain attributes such as the creation times of the files. Instead, this is stored in the inodes themselves.

4. In Unix, the **reference count** is the number of **hard links** to the file. The reference count must be checked because there may be **multiple entires** that point to the **same inode**. We must not remove the inode until **all** of these entries are gone.

5. Inode-based filesystems typically divide a file system partition into block groups. Each block group will contain a **superblock** that contains information regarding the overall filesystem. This is **replicated across block groups** to **simplify recovery**. Furthermore, for each block group, we have an inode table that describes only the inodes in its group. This aims to **reduce seek time** between the inode table and the inode of relevance.

6. 

Worst cases:
    a) Read 1 byte:
        - 4 reads: read single indirect block, read double indriect, read triple indirect, read data block.
    b) Write 1 byte:
        - 4 writes: create single indirect block, create double indirect block, create triple indirect block, write data block.
        - 3 reads, 2 writes: read single indirect, read double indirect, read triple indirect, write triple indirect, write data block.
        - Other combinations are possible.

7. 512 byte blocks. Each inode has 10 direct, 1 single indirect, 1 double indirect, and 1 triple indirect block pointer.
    a) Maximum file size before:
        - Single indirect needed: (512) * 10 = 5 kilobytes
        - Double indirect needed: (512 * 10) + (512 / 4 * 512) ~= 69 kilobytes
        - Triple indirect needed: (512 * 10) + (512 / 4 * 512) + (512 / 4 * 512 / 4 * 512) ~= 8261 kilobytes

    b) Maximum file size supported:
        - (512 * 10) + (512^2 / 4) + (512^3 / 4^2) + (512^4 / 4^3) = 1056837 kilobytes

    c) Number of disk block reads required to read 1 byte from a file
        - Best case: 1 read.
        - Worst case: 4 reads.

    d) Number of disk block reads and writes required to write 1 block to a file.
        - Best case: 1 write.
        - Worst case:
            - 4 writes: create single indirect, create double indirect, create triple indirect, write data block.
            - 3 reads, 2 writes: read single indirect, read double indirect, read triple indirect, write triple indirect, write data block.
            - Other combinations possible.

8. Block count is only indirectly related to file size.
    - Blocks used to store a file includes any indirect blocks used by the filesystem to **keep track of the file data blocks** themselves.
    - File systems only store blocks that actually contain file data. **Sparsely populated** files can have large regions that are **unused within a file**.

9. Deleting a file consists roughly of the 3 steps:
    - Remove the directory entry.
    - Mark the inode as free.
    - Mark disk blocks as free.

    No matter the ordering of the steps, we will run into problems if the process doesn't complete entirely.

    If a crash happens in the given order after the first step, then the inode and data blocks are essentially lost with **no references** to them. But they are **not marked free** by the file system.

10. EXT3 uses **journalling** which writes down the block operations (which forms a **transaction**) to be taken **before performing the block updates**. If any outage occurs during this process, the filesystem can simply read the journal and replay the transaction.