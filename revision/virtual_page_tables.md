# Virtual Page Tables
1. A VLA is a contiguously allocated range of **virtual memory** where **only needed parts** of the table **are allocated**.

When a page fault occurs:
    - Virtual address is used to index into the entire VLA.
    - If indexed into unmapped part of PT, **secondary page fault** is triggered.
        - Load mapping for PT from **root PT**.
        -Root PT is kept in **physical memory** (cannot trigger page faults).
            - Contains mapping to **pages for the virtual page table** (not the entire virtual address space).

2. VLAs are stored in virtual memory so **unused sections do not need to be allocated** physical memory. Typically, only parts of the address space is used, so a VLA will increase the size of the page table **relative to address space usage** as opposed to relative to the entire virtual address space.

3. Accessing the VLA itself can trigger a nested **TLB miss**. On the R3000 this goes through the **slow general exception handler** which is a performance issue. Sparse address space layouts exacerbate this issue as they require more TLB entries for page tables to be in TLB.