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


## Cite
If you use PLCSage for your research, please cite [Mismatched Control and Monitoring Frequencies: Vulnerability, Attack, and Mitigation](https://ieeexplore.ieee.org/document/10495752).

```
bibtex
@article{yang2024mismatched,
  title={Mismatched Control and Monitoring Frequencies: Vulnerability, Attack, and Mitigation},
  author={Yang, Zeyu and He, Liang and Cheng, Peng and Chen, Jiming},
  journal={IEEE Transactions on Dependable and Secure Computing},
  year={2024},
  publisher={IEEE}
}
```