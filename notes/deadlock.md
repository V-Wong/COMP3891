# Deadlock
## Resources
Examples of computer resources:
- Printers
- Tape drivers
- Tables in databases.

Processes need access to resources in a **reasonable order**.
- **Preemptable** resources **can be taken away** from a process with no ill effects.
- **Non-preemptable** resource will cause the process to **fail when taken away**.

## Formal Definition of Deadlock
A set of proceses is **deadlocked** if each process **in the set is waiting** for an event that only another **process in the set can cause**.

## Conditions for Deadlock
- **Mutual exclusion** condition.
    - Each resource assigned to 1 process or is available.
- **Hold and wait** condition.
    - Process holding resources can request additional resources.
- **No preemption** condition.
    - Previously granted resoucre cannot be forcibly taken away.
- **Circular wait** condition.
    - Must be a circular chain of 2 or more processes.
    - Each is waiting for resource held by next member of the chain.

## Deadlock Prevention
Must attack **one** of the four deadlock conditions.

### Attacking Mutual Exclusion
Not viable - some resources are intrinsically not shareable.

### Attacking Hold and Wait
- Require process to request resources **before starting** and then let it **run to completion**.
    - Process never has to wait for what it needs.

- Problems:
    - May **not know required resources** at start of run.
        - => Not always possible.
    - **Ties up resources** other processes could be using.
        - E.g. A process reads data from an input tape for an hour. No other process can use it in the meantime.

### Attacking No-Preemption
- Forcibly **take away resources** from a process.
- Clearly not viable:
    - Can't stop a printing job halfway through.

### Attacking Circular Wait
- ***Order** acquisition of resources such that deadlocks cannot happen.
- Resource allocation graph must be **acyclic**.

## Deadlock Detection and Recovery
Instead of preventing deadlocks, **detect** when a system is deadlock and **recover** from it.

### Detection With One Resource of Each Type
![](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXj6r7YlfWZH-f97Uq_qQkMU1CxHn5k14ETw&usqp=CAU)
- Circles are processes.
- Squares are resources.
- Process <- Resource means process holds resource.
- Process -> Resource means process requesting resource.

**Deadlock** found when there is a **cycle** in the graph.

### Detection With Multiple Resource of Each Type
![](https://thelinuxos.com/wp-content/uploads/2019/08/existence.png)

**Algorithm:**
1. Lock for an unmarked process Pi, for which the i-th row of R is less than or equal to A.
2. If found, add the i-th row of C to A, and mark Pi. Repeat from step 1.
3. If no such process exists, terminate.

**Recovery:**
- Recovery through preemption.
- Recovery through rollback.
- Recovery through killing processes.

## Deadlock Avoidance
Avoid deadlocks ahead of time.
- Requires **maximum** number of each resource required.

### Resource Trajectory
![](https://lh3.googleusercontent.com/proxy/hJXxOWpuIboMBjxFEAW4YgxKbXDWce_fQXkGzatmjt1OXrswJLFy1JDc3ZwV_gXT2UanEm0dxFs_8jz02QYhrc-TnTed__RWN1C3TRDdvPyZvGK-UJeg75SiZGGHk6Ng8EKtBZUIVSa0leKF5Ws)

- Horizontal axis represents number of instructions executed by process A.
- Vertical axis represents number of instructions executed by process B.
- Process A requests a printer at I1 and releases the printer at I3.
- Shaded regions indicate both processes having some resource.
    - Mutual exclusion makes it impossible enter these regions.

If a **trajectory** has no choice but to enter the shaded boxes, then it is **deadlocked**. 
- The box bounded by I1-I2 and I5-I6 is **unsafe**.

Trajectories must be chosen to completely **avoid unsafe regions**.
- B is requesting the plotter at t. The system must not grant it and instead suspend B to avoid deadlocks.

### Safe and Unsafe States
A state is **safe** if:
- The system is **not deadlocked**.
- There **exists a scheduling order** that results in **every process running to completion**, even if they all **request their maximum resources** immediately.

Note:
- Unsafe states are not necessarily deadlocked.
    - With a **lucky sequence**, all processes may complete.
    - However, we **cannot guarantee** that they will complete.
- Safe states **guarantee** we will eventually complete all processes.

