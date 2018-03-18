# ZeroLeptonCombination

Code is branched + slightly modified from Shun Adachi's original code. Please look at old_README.

To make combined contour plots:

* clone ZeroLeptonAnalysis
```{r, engine='bash', count_lines}
cd ZeroLeptonAnalysis
source RJRsetup.sh
cd ../../../
cd ZeroLeptonCombination
```
* Assumes file structure:
* ZeroLeptonCombination/Direct/RJR/GG/ = input directory for RJR harvest files (output of makeContours_Run2.py in ZeroLeptonAnalysis/macros/contourplot)
* ZeroLeptonCombination/Direct/MEff/GG/ = input directory for MEff harvest files

To pick out best points between RJR, MEff:

* open myCombineHarvest.py
    * params:
    * signal (line 8)
    * MEff, RJR input directories (line 10, 16)

```{r, engine='bash', count_lines}
python myCombineHarvest.py
```

* open myCombineHarvestErrors.py
* params:
    * signal, up or down error (lines 8,9)
    * MEff, RJR input directories (line 12, 18)

For both up/down errors:
```{r, engine='bash', count_lines}
python myCombineHarvestErrors.py 
```

* open run
* change signal region to be the desired signal (e.g., GG)

