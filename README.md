# Cache Simulator

## Description
- Project done as part of my Parallel Architecture Coursewrok 2
- Objctive is to simulate the operation of a Cache System
- Trace files are provided in order to perform the simulation
- Sytem simulated consists of:
    - 4 Processors 
    - Each Processor has a cache with:
        - 512 line
        - 4 words per line
    - 1 memory controller with a Direcotry
    - Protocol used: MSI
## Techincal 
Some technical stuff 
### Latencies
- Cache Probe (Tag and State access):         1 cycle(s)
- Cache Access (Read or Write):               1 cycle(s)
- Extra SRAM Access:                          1 cycle(s)
- Directory Access:                           1 cycle(s)
- One Hop between Processors:                 3 cycle(s)
- One Hop between a Processor and Directory:  5 cycle(s)
- Memory Access latency:                      15 cycle(s)

### How to use
- to run full simulation: "python main.py"
- tun run tests: "python -m unittest discover Tests"
