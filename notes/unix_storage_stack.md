# Unix Storage Stack

|Level|Description|
|-|-|
|Application|Syscall interface: ``create``, ``open``, ``read``, ``write``, ..... .|
|File descriptor table|Table of unique identifiers (handles) for open files for a given process.|
|Open file table|Global table of open files (vnodes).|
|Virtual file system|Unified interface for multiple file systems.|
|File system|Hides physical location of data on disk. Exposes directory hierarchy, symbolic file names, random access files, protection.|
|Buffer cache|Keep recently accessed disk blocks in memory.|
|Disk scheduler|Schedule disk accesses from multiple processes for performance and fairness.|
|Device driver|Hides device-specific protocol. Exposes block-device interface (linear sequence of blocks).|
|Disk controller|Hides disk geometry and exposes a linear sequence of blocks.|
|Hard disk platters|Contains tracks and sectors. Not too relevant for this course.|
