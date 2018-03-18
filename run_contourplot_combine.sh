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

cp -v summary_harvest_tree_description_MEffRJRCombine.py summary_harvest_tree_description.py
cp -v summary_harvest_tree_description_MEffRJRCombine.h summary_harvest_tree_description.h

cp ${GRID}_direct_MEffRJRCombined_fixSigXSecNominal__1_harvest_list Direct/Combined/
mv ${GRID}_direct_MEffRJRCombined_fixSigXSecUp__1_harvest_list Direct/Combined/
mv ${GRID}_direct_MEffRJRCombined_fixSigXSecDown__1_harvest_list Direct/Combined/

# use new interpolated TGraph
#:<<"#_COMMENT_"
./myHarvestToContours.py --inputFile "Direct/Combined/${GRID}_direct_MEffRJRCombined_fixSigXSecNominal__1_harvest_list" --outputFile "${GRID}_direct_MEffRJRCombined_fixSigXSecNominal__1_harvest_list.root " --interpolation linear
./myHarvestToContours.py --inputFile "Direct/Combined/${GRID}_direct_MEffRJRCombined_fixSigXSecUp__1_harvest_list"      --outputFile "${GRID}_direct_MEffRJRCombined_fixSigXSecUp__1_harvest_list.root " --interpolation linear
./myHarvestToContours.py --inputFile "Direct/Combined/${GRID}_direct_MEffRJRCombined_fixSigXSecDown__1_harvest_list"    --outputFile "${GRID}_direct_MEffRJRCombined_fixSigXSecDown__1_harvest_list.root " --interpolation linear

./myHarvestToContours.py --inputFile "Direct/RJR/${GRID}/${GRID}_direct_combined_fixSigXSecNominal__1_harvest_list"  --outputFile "output_RJR.root " # --interpolation linear
./myHarvestToContours.py --inputFile "Direct/MEff/${GRID}/${GRID}_direct_combined_fixSigXSecNominal__1_harvest_list" --outputFile "output_MEff.root " # --interpolation linear

mkdir -v $PLOTDIR
root -l -q -b "makecontourplots_CLs_combine.C(\"${GRID}_direct\",\".\",\"$PLOTDIR\", 0, $UNBLIND, \"$LUMI\", 0, 1 )" 2>&1 | tee makecontoursplots_CLs_${TYPE}.out
root -l -q -b "makecontourplots_CLs_combine.C(\"${GRID}_direct\",\".\",\"$PLOTDIR\", 1, $UNBLIND, \"$LUMI\", 0, 1 )" 2>&1 | tee makecontoursplots_CLs_${TYPE}.out
root -l -q -b "makecontourplots_CLs_combine.C(\"${GRID}_direct\",\".\",\"$PLOTDIR\", 2, $UNBLIND, \"$LUMI\", 0, 1 )" 2>&1 | tee makecontoursplots_CLs_${TYPE}.out
# #_COMMENT_
