# Description
This directory hold the extra functionality added to the code
## Changes
- Depedning on input parameters it can run the following features:
    - MSI 
    - MESI
    - Data forwarding in both directions
- These determine what features are used:
    - MESI (bool): False (default- will run MSI); True (if you want MESI)
    - FLOPER (bool): False (default- one direction for data forwarding); True (forward and backward)

# Results:
## No Optimizations:
### Trace 1
- Default info
    - Private-accesses:         179440
    - Remote-accesses:          8427
    - Off-chip-accesses:        8741
    - Total-accesses:           196608
    - Replacement-writebacks:   6357
    - Coherence-writebacks:     51
    - Invalidations-sent:       51
    - Average-latency:          3.718292236328125
    - Priv-average-latency:     2.0
    - Rem-average-latency:      14.082947668209327
    - Off-chip-average-latency: 29.0
    - Total-latency:            731046
- EXTRA INFO
    - Compulsory Misses:          2048
    - Conflic Misses:             0
    - 1 Hops                      150
    - 2 Hops                      0
    - 3 Hops                      0
    - Read Misses                 8840
    - Write Misses                8328
    - Read Hits                   155000
    - Write Hits                  24440
    - No Sharers on Read Miss     8741
    - No Sharers on Write Miss    8277
### Trace 2
- Default info:
    - Private-accesses:         491511
    - Remote-accesses:          91537
    - Off-chip-accesses:        507
    - Total-accesses:           583555
    - Replacement-writebacks:   0
    - Coherence-writebacks:     39537
    - Invalidations-sent:       52559
    - Average-latency:          5.1703369862309465
    - Priv-average-latency:     2.0
    - Rem-average-latency:      22.061581655505424
    - Off-chip-average-latency: 29.0
    - Total-latency:            3017176

- EXTRA INFO
    - Compulsory Misses:          1552
    - Conflic Misses:             0
    - 1 Hops                      22512
    - 2 Hops                      31378
    - 3 Hops                      37610
    - Read Misses                 50524
    - Write Misses                41520
    - Read Hits                   456569
    - Write Hits                  34942
    - No Sharers on Read Miss     277
    - No Sharers on Write Miss    267

### Validation
- Default info: 
    - Private-accesses:         7
    - Remote-accesses:          8
    - Off-chip-accesses:        3
    - Total-accesses:           18
    - Replacement-writebacks:   2
    - Coherence-writebacks:     1
    - Invalidations-sent:       6
    - Average-latency:          14.722222222222221
    - Priv-average-latency:     2.0
    - Rem-average-latency:      20.5
    - Off-chip-average-latency: 29.0
    - Total-latency:            265

- EXTRA INFO
    - Compulsory Misses:          4
    - Conflic Misses:             2
    - 1 Hops                      5
    - 2 Hops                      1
    - 3 Hops                      2
    - Read Misses                 5
    - Write Misses                6
    - Read Hits                   5
    - Write Hits                  2
    - No Sharers on Read Miss     1
    - No Sharers on Write Miss    0

## With Optimizations
### Trace 1
- Private-accesses:         187717
- Remote-accesses:          150
- Off-chip-accesses:        8741
- Total-accesses:           196608
- Replacement-writebacks:   6357
- Coherence-writebacks:     51
- Invalidations-sent:       51
- Average-latency:          3.213104248046875
- Priv-average-latency:     2.0
- Rem-average-latency:      18.66
- Off-chip-average-latency: 29.0
- Total-latency:            631722

### Trace 2
- Private-accesses:         491548
- Remote-accesses:          91500
- Off-chip-accesses:        507
- Total-accesses:           583555
- Replacement-writebacks:   0
- Coherence-writebacks:     39537
- Invalidations-sent:       52559
- Average-latency:          5.169576132498222
- Priv-average-latency:     2.0
- Rem-average-latency:      22.064841530054643
- Off-chip-average-latency: 29.0
- Total-latency:            3016732

