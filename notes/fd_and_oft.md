# File Descriptors and Open File Table
## File Descriptors
- Each open file has a **file descriptor**.
- ``read``, ``write``, ``lseek`` use them to specify which file to operate on.
- State associated with a file desciptor:
    - **File pointer**:
        - Determines where in the file the next read or write is performed.
    - **Mode**:
        - Read only/writeable, etc....

## File Descriptor Table Implementations
### Single Global Open File Array
- FD is an **index** into the **global** open file array. 
- Entries contain file pointer and pointer to a vnode.

Issues:
- File descriptor 1 is STDOUT.
    - Console for some processes.
    - File for others.
- Entry 1 needs to be different per process.

### Per-process File Descriptor Array
- Each process has its **own open file array**. 
- FD 1 can point to any vnode for each process.

Issues:
- Fork defines that the child **shares** the file pointer with the parent.
- Per-process table only allows for **independent file pointers**.

### Per-process File Descriptor Table With Global Open File Table
- Each process has **own file descriptor array** which contains pointers to an open file table entry.
- **Global open file table** contains entries with a fp and a pointer to a vnode.

Provides:
- Shared file pointers if required.
- Independent file pointers if required.