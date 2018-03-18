#!/bin/bash

GRID=GG
PLOTDIR=plots
UNBLIND=1
:<<"#_COMMENT_"
SigXSec=(
"fixSigXSecNominal" 
"_fixSigXSecUp"
"_fixSigXSecDown"
);
#_COMMENT_
# SigXSec=(
# "fixSigXSecNominal" 
# );
LUMI=36.1ifb

# Please check input path in myCombineHarvest.py
# ./myCombineHarvest.py


mkdir -v oneStep/Combined/
cp -v ${GRID}_onestepCC_MEffRJRCombined_fixSigXSecNominal__mlspNE60_harvest_list oneStep/Combined/
cp -v ${GRID}_onestepCC_MEffRJRCombined_fixSigXSecUp__mlspNE60_harvest_list oneStep/Combined/
cp -v ${GRID}_onestepCC_MEffRJRCombined_fixSigXSecDown__mlspNE60_harvest_list oneStep/Combined/

cp -v summary_harvest_tree_description_MEffRJRCombined_${GRID}onestepCC.py summary_harvest_tree_description.py
cp -v summary_harvest_tree_description_MEffRJRCombined_${GRID}onestepCC.h summary_harvest_tree_description.h


# use new interpolated TGraph
#:<<"#_COMMENT_"
./myHarvestToContours.py --inputFile "oneStep/Combined/${GRID}_onestepCC_MEffRJRCombined_fixSigXSecNominal__mlspNE60_harvest_list" --outputFile "${GRID}_onestepCC_MEffRJRCombined_fixSigXSecNominal__mlspNE60_harvest_list.root " --interpolation linear
./myHarvestToContours.py --inputFile "oneStep/Combined/${GRID}_onestepCC_MEffRJRCombined_fixSigXSecUp__mlspNE60_harvest_list" --outputFile "${GRID}_onestepCC_MEffRJRCombined_fixSigXSecUp__mlspNE60_harvest_list.root " --interpolation linear
./myHarvestToContours.py --inputFile "oneStep/Combined/${GRID}_onestepCC_MEffRJRCombined_fixSigXSecDown__mlspNE60_harvest_list" --outputFile "${GRID}_onestepCC_MEffRJRCombined_fixSigXSecDown__mlspNE60_harvest_list.root " --interpolation linear

./myHarvestToContours.py --inputFile "oneStep/RJR/${GRID}/${GRID}_onestepCC_combined_fixSigXSecNominal__mlspNE60_harvest_list" --outputFile "output_RJR.root " --interpolation linear
./myHarvestToContours.py --inputFile "oneStep/MEff/${GRID}/${GRID}_onestepCC_combined_fixSigXSecNominal__mlspNE60_harvest_list" --outputFile "output_MEff.root " --interpolation linear


mkdir -v $PLOTDIR
root -l -q -b "makecontourplots_CLs_combine_onestep.C(\"${GRID}_onestepCC\",\".\",\"$PLOTDIR\", 0, $UNBLIND, \"$LUMI\", 0, 1 )" 2>&1 | tee makecontoursplots_CLs_${TYPE}.out
root -l -q -b "makecontourplots_CLs_combine_onestep.C(\"${GRID}_onestepCC\",\".\",\"$PLOTDIR\", 1, $UNBLIND, \"$LUMI\", 0, 1 )" 2>&1 | tee makecontoursplots_CLs_${TYPE}.out
root -l -q -b "makecontourplots_CLs_combine_onestep.C(\"${GRID}_onestepCC\",\".\",\"$PLOTDIR\", 2, $UNBLIND, \"$LUMI\", 0, 1 )" 2>&1 | tee makecontoursplots_CLs_${TYPE}.out
#_COMMENT_
