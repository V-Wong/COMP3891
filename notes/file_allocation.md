# File Allocation Strategies
## Implementation Considerations
- FS must map **symbolic file names** into a collection of **block addresses**.
- FS must keep track of:
    - Which blocks belong to which files.
    - What order the blocks form the file.
    - Which blocks are free for allocation.
- Given a **local region of a file**, the FS must track to **corresponding block(s)** on the disk.
    - Stored in FS metadata.

## Contiguous Allocation
Pros:
- Easy bookkeeping
    - Track starting block and length of file.
- Increases performance for **sequential operations**.

Cons:
- Need to **know maximum size** of file at creation.
- Free space becomes many small chunks as files are deleted (**external fragmentation**)

## Dynamic Allocation: Linked List
Each block contains pointer to next block in chain. Free blocks also linked in a chain.

Pros:
- Only **single metadata** entry per file (starting block).
- Best for **sequential files**.

Cons:
- Poor **random access**.
- Blocks end up **scattered across disk** due to free list eventually being randomised.

## Dynamic Allocation: File Allocation Table
Keep a **map of entire FS** in a **separate table**.
- A table entry contains the address (index) number of the next block of the file.
- The last block in a file and empty blocks are marked using reserved values.

Table is stored on the disk and is replicated in memory.

Pros:
- **Random access** is fast (follow in-memory list).

Cons:
- Requires a **lot of memory** for large disks.
- **Free block lookup is slow.**
    - Must linear scan for free entry in table.

## Dynamic Allocation: Inode-based
Keep separate table (inode) for **each file**.
- Only keep table for open files in memory.
- Fast random access

Free space management:
- **Linked list of free blocks** in free blocks on disk.
    - List of all unallocated blocks.
    - Background jobs can reorder list for better contiguity.
    - STore in free blocks themselves to not reduce disk capacity.
    - Only one block of pointers need to be kept in main memory.
- **Bitmap of freeblocks** on disk.
    - Individual bits in a bit vector.
    - May be **too large** to hold in main memory.
    - Expensive to search.
    - Concentrating (de)allocations in a portion of the bitmap has desirable effect of **concentrating access**.
    - Simple to find **contiguous free space**.


