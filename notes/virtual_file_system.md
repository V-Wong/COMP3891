# Virtual File System
## Overview
Aim is to provide a framework that separates **file system independent** and **file system dependent code**.

- Provides **single syscall interface** for **many file systems**.
    - E.g. UFS, Ext2, ....
- Transparent handling of network file systems
    - E.g. NFS, AFS, CODA.
- File-based interface to arbitrary device drivers.
- File-based interface to kernel data structures.
- Provides an **indirection layer** for system calls.
    - File operation table set up at file open time.
    - Points to actual handling code for particular type.
    - Further file operations redirected to those functions.

## Interface
- VFS
    - Represents all file system types.
    - Contains pointers to functions to manipualte each file system as a whole (e.g. mount and unmount).
        - Form a standard interface to the file system.

- Vnode
    - Represents a file (inode) in the underlying filesystem.
    - Points to the real inode.
    - Contains pointers to functiosn to manipulate files/inodes (e.g. open, close, read, write....).
