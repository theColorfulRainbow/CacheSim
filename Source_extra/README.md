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
## Trace 1
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

## Trace 2
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

