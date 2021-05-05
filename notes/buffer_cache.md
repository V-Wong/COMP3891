# Buffer Cache
## Overview
Buffer is **temporary storage** used when transferring data **between two entities**.
    - Especially when entities work at **different rates**.
    - Or when the unit of transfer is incompatible.
        - E.g. between application program and disk.

## Buffering Disk Blocks
- **Whole blocks** are transferred from disk to a **buffer in kernel ram**.
- **Arbitrarily sized regions** are then transferred from the buffer to application memory.

## Cache
Cache is **fast storage** used to **temporarily hold data** to **speed up repeated access** to the data.

### Caching Disk Blocks
Disk blocks are cahced in kernel ram.

- Before loading block from disk, check if it is in cache first.
    - Avoids disk accesses.
    - Can optimise for repeated access for single or several processes.

### Unix Buffer Cache
On read:
- Hash the device and block number.
- Check if match in buffer cache.
    - Yes, simply use in memory copy.
    - No, follow collision chain.
        - If not found, load block from disk into buffer cache.

#### Buffer Replacement
Entry must be **replaced if cache is full** and we need to read another block into memory.
- If block in cache has been modified, must be written back to disk.

Policies:
- First-in First-out.
- Least Recently Used.

#### Consistency Considerations:
Cached disk blocks prioritised in terms of how **critical** they are **to the file system**.

- Directory blocks, inode blocks if lost can **corrupt entire filesystem**.
    - Usually scheduled for **immediate write** to disk.
- Data blocks if lost corrupt only the file they are associated with.
    - Scheduled for write to disk **periodically**.

Alternatively, use a **write-through cache** that writes modified blocks to disk **immediately**.