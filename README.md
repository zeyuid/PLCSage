# PLCSage
Seeing Is Not Believing: Exploiting Mismatched Control and Monitoring Frequencies to Mount Stealthy Attacks in Industrial Control Systems


## Identify physical signals
1. Obtain the Entropy bit state transition: 

python ./data_segmentation/data_extraction.py

2. Obtain the value of identified PLC variables, with varying alpha_list and beta_list

python ./data_segmentation/segmenting_utils.py

## Attack detection in SCADA

python ./customized_SCADA.py


## Mount stealthy attack 

python ./stealthy_attack.py

The exploitation of "Force" function for Siemens PLC and Rockwell PLC is coming soon!
