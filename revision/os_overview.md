# Operating Systems Overview
1.
- **Abstract (Extended) Machine**
    - OS provides **abstractions** that hide the details of the underlying hardware.
    - Allows applications to be written with **little concern to the hardware** it is running on. 
    - Allows for **more portable code** that can be run on a variety of hardware with no modifications.

- **Resource Manager**
    - OS is responsible for effectively utilising the hardware available to it.
    - Involves dividing resources to processes according to some policy that ensures **fairness**, **isolation** and **efficiency**.

2. 
- In **priviledge mode**:
    - All instructions of the architecture are available.
    - All memory addresses are accessible.

- In **user mode**:
    - Only a subset of the architecture instructions are available.
        - Kernel doesn't trust application to not perform something malicious and crash the entire system.
    - Only a subset of the memory is accessible.
        - Kernel does not trust applications not to corrupt their memory.

The two modes are required to ensure applications does not bypass, circumvent or **take control of the OS**.