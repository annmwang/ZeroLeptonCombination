#!/usr/bin/env python

import os, sys, shutil
from ROOT import *

harvestFile  ="summary_harvest_tree_description.py"

# change me
signal = "GG"
errors = "Up" #"Down"

MEffInputDir = "Direct/MEff/"+signal
MEffFile     = signal + "_direct_combined_fixSigXSecNominal__1_harvest_list"
MEffInputFile= MEffInputDir + "/" + MEffFile
MEffInfoFile = MEffInputFile+"_infoFile";
MEffHarvest  = MEffInputDir + "/" + harvestFile

RJRInputDir  = "Direct/RJR/"+signal
RJRFile      = signal+"_direct_combined_fixSigXSecNominal__1_harvest_list"
RJRInputFile = RJRInputDir + "/" + RJRFile
RJRInfoFile = RJRInputFile+"_infoFile";
RJRHarvest   = RJRInputDir + "/" + harvestFile

# trying to fix stuff
RJRErrFile      = signal+"_direct_combined_fixSigXSec"+errors+"__1_harvest_list"
RJRErrInputFile = RJRInputDir + "/" + RJRErrFile
RJRErrInfoFile = RJRErrInputFile+"_infoFile";

MEffErrFile      = signal+"_direct_combined_fixSigXSec"+errors+"__1_harvest_list"
MEffErrInputFile = MEffInputDir + "/" + MEffErrFile
MEffErrInfoFile = MEffErrInputFile+"_infoFile";

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
    os.mkdir("Direct/Combined")
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
  CLsindexMEff = myMEffvars.index("CLs/F")
  fIDindexMEff = myMEffvars.index("fID/C")
  upperLimitindexMEff = myMEffvars.index("upperLimit/F")
  
  m0indexRJR = myRJRvars.index("m0/F")
  m12indexRJR = myRJRvars.index("m12/F")
  CLsexpindexRJR = myRJRvars.index("CLsexp/F")
  CLsindexRJR = myRJRvars.index("CLs/F")
  fIDindexRJR = myRJRvars.index("fID/C")
  upperLimitindexRJR = myRJRvars.index("upperLimit/F")
  
  
  outputfilename = MEffErrInputFile.split("/")[-1].replace("_combined_","_MEffRJRCombined_");
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
  
  MEffNomLines = open(MEffInputFile).readlines()
  MEffErrLines = open(MEffErrInputFile).readlines()
  RJRNomLines = open(RJRInputFile).readlines()
  RJRErrLines = open(RJRErrInputFile).readlines()
  
  myMap = {}

  for i, MEffline in enumerate(MEffNomLines):

    MEffNomline = MEffNomLines[i].strip()
    MEffNomdata = MEffNomLines[i].split()
  
    for j, RJRline in enumerate(RJRNomLines):
  
      RJRNomline = RJRNomLines[j].strip()
      RJRNomdata = RJRNomLines[j].split()
  
      RJRNomdata[fIDindexRJR] = str(int(RJRNomdata[fIDindexRJR])+100)
      RJRNomline = " ".join(RJRNomdata)
  
      if MEffNomdata[m0indexMEff]!=RJRNomdata[m0indexMEff]:
        continue
      if MEffNomdata[m12indexMEff]!=RJRNomdata[m12indexMEff]:
        continue
  
      if float(MEffNomdata[CLsexpindexMEff]) < float(RJRNomdata[CLsexpindexRJR]):
#      if float(MEffNomdata[CLsexpindexMEff]) < float(RJRNomdata[CLsexpindexRJR]) or (int(float(MEffNomdata[m0indexMEff])) == 25 and int(float(MEffNomdata[m12indexMEff])) == 1125):
        key = "%s_%s" % (MEffNomdata[m0indexMEff], MEffNomdata[m12indexMEff])
        myMap[key] = "MEff"
      elif float(MEffNomdata[CLsexpindexMEff]) >= float(RJRNomdata[CLsexpindexRJR]):
        key = "%s_%s" % (RJRNomdata[m0indexRJR], RJRNomdata[m12indexRJR])
        myMap[key] = "RJR"
        pass;
  
      pass;
  
    pass;
  pass;

  for i, MEffline in enumerate(MEffErrLines):

    MEffline = MEffline.strip()
    MEffdata = MEffline.split()
  
    for j, RJRline in enumerate(RJRErrLines):
  
      RJRline = RJRline.strip()
      RJRdata = RJRline.split()
  
      RJRdata[fIDindexRJR] = str(int(RJRdata[fIDindexRJR])+100)
      RJRline = " ".join(RJRdata)
  
      if MEffdata[m0indexMEff]!=RJRdata[m0indexMEff]:
        continue
      if MEffdata[m12indexMEff]!=RJRdata[m12indexMEff]:
        continue
  
      key = "%s_%s" % (MEffdata[m0indexMEff], MEffdata[m12indexMEff])
      if myMap[key] == "MEff":
        outputfile.write(modifyLine(MEffline,myMEffvars,combinevars)+'\n')
      elif myMap[key] == "RJR":
        outputfile.write(modifyLine(RJRline,myRJRvars,combinevars)+'\n')
        pass;
  
      pass;
  
    pass;
  
  outputfile.close()


if __name__ == "__main__":
	main()
