#include <vector>
#include "TPRegexp.h"
//#include "contourmacros/SUSY_contourplots.C"
#include "contourmacros/SUSY_contourplots_old.C"

void makecontourplots_CLs_combine_onestep(const TString Grid="GG_direct",TString dirname = ".",TString outdir="plots_combine",int showSR=0,bool unblind=true, TString lumi="11.8ifb", bool showAllSRExp=false, bool useTGraph=false) 
{
  int  discexcl(1); // 0=discovery, 1=exclusion
  bool drawOldLimits(true);
  vector<TString> infilelist;
  vector<TString> inlist;

  if(showAllSRExp) drawOldLimits = false;

  // XSec Nominal Up Down
  TString combined[3]={ "MEffRJRCombined_fixSigXSecNominal__mlspNE60_harvest_list", 
                        "MEffRJRCombined_fixSigXSecUp__mlspNE60_harvest_list",
                        "MEffRJRCombined_fixSigXSecDown__mlspNE60_harvest_list"};
  //TString combined[3]={"combined_Nominal", "combined_Nominal","combined_Nominal"}; // no xsection error

  for(int i=0; i<3; i++){
     infilelist.push_back(dirname+"/"+Grid+"_"+combined[i]+".root");
     cout<< infilelist[i]<<" ";
  }
  cout<<endl;
  
  lumi=lumi.ReplaceAll("ifb","");
  cout<<"lumi="<<lumi<<" fb-1"<<endl;
  (void) SUSY_contourplots(
      infilelist.at(0), infilelist.at(1), infilelist.at(2),
      "0-leptons, 2-6 jets", 
      lumi,
      Grid,
      outdir,
      showSR,
      unblind,
      showAllSRExp,
      drawOldLimits,
      useTGraph,
      discexcl=1);
}

