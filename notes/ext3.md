# EXT3 File System
## Overview
Design goals:
- Add **journalling** capability to the EXT2 FS.
- Backward and forward compatibility with EXT2.

## Journal
### Disk Block Updates
Example:
- Start transaction.
- Update block #n1 (contains directory entry).
- Update block #n2 (inode allocation bitmap).
- Update block #n2 (data block allocation bitmap).
- End transaction.

Advantages:
- Multiple update to the same block can be **aggregated into a single update**.
- Journalling layer is FS-independent.

Disadvantage:
- Even a small update adds a **whole block** to the journal.

## Journal Block Device
### Transaction Lifecycle
|Stage|Description|
|-|-|
|**In progress**|Updates are buffered in RAM.|
|**Completed**|Updates are buffered in RAM; no additional updates are allowed in the same transaction.|
|**Committed**|Updates are written to the journal and marked as committed. Transaction can be replayed after an unclean unmount.|
|**Checkpointed**|Updates are written to the file system; the transcation is removed from the journal.|

## Journaling Modes
EXT3 supports two journalling modes:
- **Metadata + data**:
    - **Enforces atomicity** of all FS operations.
- **Metadata journalling**:
    - Metadata is journalled.
    - Data blocks are written directly to the disk.
    - Improves **performance**.
    - Enforces file system integrity.
    - **Does not enforce atomicity** of ``write``.
        - New file content can be stale blocks.