


 TString infile0 ="SS_onestepCC_contours.root";
 TString outfile0="SS_onestepCC_2015.root";

 //TString infile0 ="SM_GG_N2_contours.root";
 //TString outfile0="SM_GG_N2_2015.root";
 
 TString ingraphName  = "gcontour_obscls_0";
 

TString outgraphName = "observed"         ;


void Rename(TString infilename=infile0, TString outfilename=outfile0){

   TFile* outfile = new TFile(outfilename,"recreate");
   TFile* infile  = new TFile(infilename);

   TGraph* graph = (TGraph*)infile->Get(ingraphName);
   graph->SetName(outgraphName);

   outfile->cd();
   graph->Write();
   outfile->Close();
   delete outfile;

   infile->Close();
   delete infile;

}


