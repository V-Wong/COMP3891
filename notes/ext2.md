# EXT2 File System
## Overview
Features:
- Block size (1024, 2048, and 4096) configured at FS creation.
- inode-based FS.
- Performance optimisations to improve locality.

Main problem:
- Unclean unmount requires e2fsck.

## Structure of Inodes
|Field name|Description|
|-|-|
|``mode``|Type: regular file or directory. Access mode: read/write etc...|
|``uid``|User id.|
|``gid``|Group id.|
|``mtime``|Last modified time.|
|``size``|Offset of the highest byte written.|
|``block_count``|Number of disk blocks used by the file. Note: can be much less expected given the file size if the file is sparsely populated.|
|``reference_count``|Needed because files with different names may be linked to the same inode.|
|``direct_blocks``|Block numbers of first 12 blocks in the file.|
|``single_indirect_blocks``|Block number of a block containing block numbers|
|``double_indirect_blocks``|Block number of a block containing block numbers of blocks containing block numbers|
|``triple_indirect_blocks``|As above, but another layer.|

## Where/How are Inodes Stored
The hard disk is partitioned into **block groups**.

### Layout of Block Group
|Region|Size|Description|
|-|-|-|
|Super Block|1 block|Contains information about the overall file system. Contains overall free inode and block counters. Contains replicated information about the file system health. (Replicated for redundancy)|
|Group Descriptors|n blocks|Location of the bitmaps. Counter for free blocks and inodes in the group. Number of directories in the group.|
|Data Block Bitmap|1 block||
|Inode Bitmap|1 block||
|Inode Table|m blocks||
|Data Blocks|k blocks|Proximity of inode table and data blocks reduces seek time.|

## Directory Implementation
Directories are just **special files**.
- Directories translate **names to inode numbers**.
- Directory entires are of variable length.
- Entries can be deleted in place.

## Performance Considerations
- Block groups **cluster related inodes and data blocks**.
- Up to 8 blocks are **preallocated** on writes.
    - Aim for better contiguity when there are concurrent writes.
- Aim to store files within a directory in the same group.

## Reliability Problems
Disk writes are buffered in RAM.
- OS crash => lost data.
- Commit writes to disk periodically.
- Use sync command to force a FS flush.

FS operations are non-atomic.
- Incomplete transaction can leave the FS in an incomplete state.