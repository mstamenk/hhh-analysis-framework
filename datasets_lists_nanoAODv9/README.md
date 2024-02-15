# Getting the lists on centrally produced samples 

To have the list of samples do, for example:

```
dasgoclient -query=dataset=/*HHHTo4B2G*/RunIISummer20UL*NanoAODv*/NANOAODSIM > datasets_lists_nanoAODv9/Run2_HHH4B2G.txt
```

==> you might need to follow steps to make a grid certificate

# List of "signals" relevant to HHH

This is what we expect in terms of signals, looking in what is avaiable to Run2 UL NanoAODv9 (to be top-up with PNet with [this](https://github.com/hqucms/nano-configs/tree/NanoAODv9-ParticleNetAK4))

- For the HHH6B
    - datasets_lists_nanoAODv9/Run2_GF_HH4B.txt  
    - datasets_lists_nanoAODv9/Run2_VBF_HH4B.txt  - I did not found the sample name
    - datasets_lists_nanoAODv9/Run2_WHH4B.txt
    - datasets_lists_nanoAODv9/Run2_ZHH4B.txt 
    - datasets_lists_nanoAODv9/Run2_HHH6B.txt  
    - datasets_lists_nanoAODv9/Run2_ttH2B.txt
    - datasets_lists_nanoAODv9/Run2_ttHH4B.txt
    - datasets_lists_nanoAODv9/Run2_VH2B.txt - I did not found the sample name
    - GF H2B? - I did not found the sample name

- For the HHH4B2Tau
    - datasets_lists_nanoAODv9/Run2_GF_HH2B2Tau.txt
    - datasets_lists_nanoAODv9/Run2_VBF_HH2B2Tau.txt - I did not found the sample name
    - datasets_lists_nanoAODv9/Run2_HHH4B2Tau.txt - couplings MISING!!!
    - datasets_lists_nanoAODv9/Run2_ttH2Tau.txt
    - datasets_lists_nanoAODv9/Run2_VH2Tau.txt
    - datasets_lists_nanoAODv9/Run2_ttHH2B2Tau.txt
    - GF H2Tau? - I did not found the sample name

- For the HHH4B2G
    - datasets_lists_nanoAODv9/Run2_GF_HH2B2G.txt
    - datasets_lists_nanoAODv9/Run2_VBF_HH2B2G.txt  - I did not found the sample name
    - datasets_lists_nanoAODv9/Run2_HHH4B2G.txt
    - datasets_lists_nanoAODv9/Run2_ttH2G.txt
    - datasets_lists_nanoAODv9/Run2_VH2G.txt
    - datasets_lists_nanoAODv9/Run2_ttHH2B2G.txt
    - GF H2G? - I did not found the sample name

Comments
-  VHH is only avaiable to 4B
- TTHH is avaiable to all final states