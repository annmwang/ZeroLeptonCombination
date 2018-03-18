#!/usr/bin/env python

import os, sys, shutil
from ROOT import *

harvestFile  ="summary_harvest_tree_description.py"

signal = "GG"

MEffInputDir = "Direct/MEff/"+signal
MEffFile     = signal+"_direct_combined_fixSigXSecNominal__1_harvest_list"
MEffInputFile= MEffInputDir + "/" + MEffFile
MEffInfoFile = MEffInputFile+"_infoFile";
MEffHarvest  = MEffInputDir + "/" + harvestFile

RJRInputDir  = "Direct/RJR/"+signal
RJRFile      = signal+"_direct_combined_fixSigXSecNominal__1_harvest_list"
RJRInputFile = RJRInputDir + "/" + RJRFile
RJRInfoFile = RJRInputFile+"_infoFile";
RJRHarvest   = RJRInputDir + "/" + harvestFile

def modifyLine(line,oldvars,newvars):
  values=line.split();
  newline="";
  for var in newvars:
    newline+=values[oldvars.index(var)]+" ";
    pass;
  newline.rstrip();
  return newline;

def modifyDescription(oldFile,newFile,combinevars):
  oldHarvest = open(oldFile);
  newHarvest = open(newFile,"w");
  changeDescription=False;
  for line in oldHarvest:
    if (not changeDescription) and ("description = " in line) :
      newdescription=":".join(combinevars);
      if newFile.endswith(r".h"):
        newHarvest.write("  const char* description = \""+newdescription+"\";\n");
      else:
        newHarvest.write("  description = \""+newdescription+"\"\n");
        pass;
      changeDescription=True;
    else:
      newHarvest.write(line);
      pass;
    pass;



def main():
  pwd = os.getcwd()
  try:
    os.mkdir(pwd+"/Direct/")
  except:
    "Folder already exists!"
  try:
    os.mkdir(pwd+"/Direct/Combined")
  except:
    "Folder already exists!"
  outputfolder = "Direct/Combined/"

  shutil.copyfile(MEffHarvest,"summary_harvest_tree_description_MEff.py");
  shutil.copyfile(MEffHarvest.replace(r".py",r".h"),"summary_harvest_tree_description_MEff.h");
  from summary_harvest_tree_description_MEff import treedescription as MEfftreedescription

  dummy, myMEffvars = MEfftreedescription()
  myMEffvars = myMEffvars.split(":")

  shutil.copyfile(RJRHarvest,"summary_harvest_tree_description_RJR.py");
  from summary_harvest_tree_description_RJR import treedescription as RJRtreedescription

  dummy, myRJRvars = RJRtreedescription()
  myRJRvars = myRJRvars.split(":")

  m0indexMEff = myMEffvars.index("m0/F")
  m12indexMEff = myMEffvars.index("m12/F")
  CLsexpindexMEff = myMEffvars.index("CLsexp/F")
  fIDindexMEff = myMEffvars.index("fID/C")
  upperLimitindexMEff = myMEffvars.index("upperLimit/F")
  xsecindexMEff = myMEffvars.index("xsec/F")
  
  m0indexRJR = myRJRvars.index("m0/F")
  m12indexRJR = myRJRvars.index("m12/F")
  CLsexpindexRJR = myRJRvars.index("CLsexp/F")
  fIDindexRJR = myRJRvars.index("fID/C")
  upperLimitindexRJR = myRJRvars.index("upperLimit/F")
  xsecindexRJR = myRJRvars.index("xsec/F")
  
  outputfilename = MEffInputFile.split("/")[-1].replace("_combined_","_MEffRJRCombined_");
  outputfile = open(outputfilename,"w")
  
  # obtain matched variables
  combinevars=[];
  for var in myMEffvars:
    if var in myRJRvars:
      combinevars.append(var);
      pass;
    pass;

  # write new summary_harvest_tree_description for combined list
  modifyDescription(MEffHarvest,"summary_harvest_tree_description_MEffRJRCombine.py",combinevars);
  modifyDescription(MEffHarvest.replace(r".py",r".h"),"summary_harvest_tree_description_MEffRJRCombine.h",combinevars);

  # make new combined SR index & new infoFile for SRName
  infoFileMEff = open(MEffInfoFile);
  infoCombine={};
  for line in infoFileMEff:
    line.strip();
    columns = line.split();
    if len(columns)>2 :
      (indexStr, colon, SRName) = columns;
      index=(int)(indexStr);
      infoCombine[index] = SRName;
      pass;
    pass;
  infoFileRJR  = open(RJRInfoFile);
  for line in infoFileRJR:
    line.strip();
    columns = line.split();
    if len(columns)>2 :
      (indexStr, colon, SRName) = columns;
      index=(int)(indexStr);
      newindex = index+100;
      infoCombine[newindex] = SRName;
      pass;
    pass;
  newInfoFile = open(outputfilename+"_infoFile", "w" );
  for i,SRName in infoCombine.items():
    newInfoFile.write( "%d : %s\n" % (i,SRName));
  newInfoFile.close();
  
  
  for MEffline in open(MEffInputFile).readlines():
  
    MEffline = MEffline.strip()
    MEffdata = MEffline.split()
  
    for RJRline in open(RJRInputFile).readlines():
  
      RJRline = RJRline.strip()
      RJRdata = RJRline.split()
  
      RJRdata[fIDindexRJR] = str(int(RJRdata[fIDindexRJR])+100)
      RJRline = " ".join(RJRdata)
  
      if MEffdata[m0indexMEff]!=RJRdata[m0indexMEff]:
        continue
      if MEffdata[m12indexMEff]!=RJRdata[m12indexMEff]:
        continue
  
      if float(MEffdata[CLsexpindexMEff]) < float(RJRdata[CLsexpindexRJR]):
        outputfile.write(modifyLine(MEffline,myMEffvars,combinevars)+'\n')
      elif float(MEffdata[CLsexpindexMEff]) >= float(RJRdata[CLsexpindexRJR]):
        outputfile.write(modifyLine(RJRline,myRJRvars,combinevars)+'\n')
        pass;
  
      pass;
  
    pass;
  
  outputfile.close()

if __name__ == "__main__":
	main()
