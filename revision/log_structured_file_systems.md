# Log Structured File Systems
1. inode-based file systems can perform poorly when writing small files because it requires **multiple writes for metadata** which may be scattered across the hard disk, requireing long seek times and rotational delays.

2. A LFS **never overwrites old blocks**, instead always writing new blocks. The LFS contains two fixed regions on the disk that contains the inode map. The LFS alternates writing between the two periodically (checkpoint) to provide some extra redundancy. If a power failure occurs, the LFS would still be consistent with the latest version of the inode-map block.

3. A file system checker is necessary because many file system operations are **not atomic**. If the system fails while halfway through the process, the system is left in an inconsistent state.

E.g.
- Delete the directory entry of the file.
- Mark the inode associated with the file as free.
- Mark the data blocks of this file as free.

4. A cleaner in a LFS is a **background job** that **cleans up unused blocks** and **compacts used blocks** into contiguous chunks. This is necessary because disks are finite in size.

The cleaner runs more often when the disk is **almost full**, degrading the performance of a log structured file system.

5. LFS **cache the metadata writes** involved in small file updates in **memory** and writes out these updates to the disk sequentially in large chunks. In contrast, inode-based file systems would write the metadata updates to disk immediately to ensure consistency, and these updates would be scattered across the disk.