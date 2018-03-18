#!/usr/bin/env python

#You'll have to have matplotlib and root setup side-by-side
#
#> localSetupSFT --cmtConfig=x86_64-slc6-gcc48-opt releases/LCG_79/pytools/1.9_python2.7,releases/LCG_79/pyanalysis/1.5_python2.7
#> lsetup root

import ROOT

import matplotlib as mpl
mpl.use('pdf')
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate

import json

import argparse
import math


parser = argparse.ArgumentParser()
parser.add_argument("--inputFile", type=str, help="input harvest file", default = "GG_direct_MEffRJRCombined_fixSigXSecNominal__1_harvest_list")
parser.add_argument("--outputFile", type=str, help="output ROOT file", default = "GG_direct_combined_Nominal.root")
parser.add_argument("--interpolation", type=str, help="type of interpolation", default = "linear") # linear, multiquadric
parser.add_argument("--level", type=float, help="contour level output", default = ROOT.RooStats.PValueToSignificance( 0.05 ))
args = parser.parse_args()


def main():

  # Step 1 - Read in harvest list in either text or json format and dump it into a dictionary
  tmpdict = harvestToDict( args.inputFile )

  addZerosToDict(tmpdict,maxyvalue = 1200)

  # Step 2 - Interpolate the fit results
  print ">>> Interpolating mass plane"
  (xi,yi,zi) = interpolateMassPlane( tmpdict , args.interpolation )


  f = ROOT.TFile(args.outputFile,"recreate")

  # from array import array

  # if np.isnan(zi["CLsexp"]).any():
  #   print "something's nan!"
  # if np.isinf(zi["CLsexp"]).any():
  #   print "something's inf!"

  # gr = ROOT.TGraph2D(len(xi),
  #   array('f',xi),
  #   array('f',yi),
  #   array('f',zi["CLsexp"] ) )


  # gr.Write()
  # f.Close()
  # return

  print ">>> Writing contours out"
  # Step 3 - get TGraph contours
  for whichEntry in ["CLs","CLsexp","clsu1s","clsu2s","clsd1s","clsd2s"]:
    contourList = getContourPoints(xi[whichEntry],yi[whichEntry],zi[whichEntry], args.level)

    graphs = []
    for i,contour in enumerate(contourList):
      # if (contour[1]>contour[0]).all():
      #   continue
      graphs.append( ROOT.TGraph(len(contour[0]), contour[0].flatten('C'), contour[1].flatten('C') )   )

    biggestGraph = 0
    for graph in graphs:
      if biggestGraph==0:
        biggestGraph = graph
      elif graph.Integral() > biggestGraph.Integral():
        biggestGraph = graph
    biggestGraph.Write("%s_Contour_0"%(whichEntry)  )

  print ">>> Closing file"

  f.Write()
  f.Close()


def harvestToDict( harvestInputFileName = "" ):
  print ">>> entering harvestToDict()"

  massPlaneDict = {}

  harvestInput = open(harvestInputFileName,"r")

  # try:
  if "oneStep/RJR/GG" in harvestInputFileName:
    print "got RJR GG"
    from summary_harvest_tree_description_RJR_onestepGG import treedescription
  elif "oneStep/RJR/SS" in harvestInputFileName:
    print "got RJR SS"
    from summary_harvest_tree_description_RJR_onestepSS import treedescription
  else:
    from summary_harvest_tree_description import treedescription
  # from summary_harvest_tree_description_MEffRJRCombine import treedescription
  dummy,fieldNames = treedescription()
  fieldNames = fieldNames.split(':')

  if ".json" in harvestInputFileName and 0:
    print ">>> Interpreting json file"

    with open(harvestInput) as inputJSONFile:
      inputJSONFile = json.load(inputJSONFile)

  else:
    print ">>> Interpreting text file"


    for massLine in harvestInput.readlines():
      values = massLine.split()
      values = dict(zip(fieldNames, values))
      print values

      print values["fID/C"]

      if "m12/F" in values:
        massPoint = (  float(values["m0/F"])  , float(values["m12/F"])   )
      elif "mgluino/F" in values:
        massPoint = (  float(values["mgluino/F"])  , float(values["mlsp/F"])   )
      elif "msquark/F" in values:
        massPoint = (  float(values["msquark/F"])  , float(values["mlsp/F"])   )


      massPlaneDict[massPoint] = {
        "CLs":        ROOT.RooStats.PValueToSignificance( float(values["CLs/F"])     ) ,
        "CLsexp":     ROOT.RooStats.PValueToSignificance( float(values["CLsexp/F"])  ) ,
        "clsu1s":     ROOT.RooStats.PValueToSignificance( float(values["clsu1s/F"])  ) ,
        "clsu2s":     ROOT.RooStats.PValueToSignificance( float(values["clsu2s/F"])  ) ,
        "clsd1s":     ROOT.RooStats.PValueToSignificance( float(values["clsd1s/F"])  ) ,
        "clsd2s":     ROOT.RooStats.PValueToSignificance( float(values["clsd2s/F"])  ) ,
      }

      print massPoint, ROOT.RooStats.PValueToSignificance( float(values["CLs/F"])     )

  return massPlaneDict


def addZerosToDict(mydict, maxyvalue = 0):
  for x in np.linspace( 0, 2000, 50 ):
    mydict[(x,x)] = {
        "CLs":    0,
        "CLsexp": 0,
        "clsu1s": 0,
        "clsu2s": 0,
        "clsd1s": 0,
        "clsd2s": 0,
      }

  # for x in np.linspace( 0, 1000, 10 ): #SS_onestep
  #   mydict[(x+10,x)] = {
  #       "CLs":    ROOT.RooStats.PValueToSignificance( 0.01 ),
  #       "CLsexp": ROOT.RooStats.PValueToSignificance( 0.01 ),
  #       "clsu1s": ROOT.RooStats.PValueToSignificance( 0.01 ),
  #       "clsu2s": ROOT.RooStats.PValueToSignificance( 0.01 ),
  #       "clsd1s": ROOT.RooStats.PValueToSignificance( 0.01 ),
  #       "clsd2s": ROOT.RooStats.PValueToSignificance( 0.01 ),
  #     }
    
  #for x in np.linspace( 0, 800, 50 ): #GG_onestep
  for x in np.linspace( 0, 400, 50 ): #SS_onestep
  #for x in np.linspace( 0, 600, 10 ): #SS_direct
  #for x in np.linspace( 0, 760, 20 ): #GG_direct
    mydict[(x,x)] = {
        "CLs":    ROOT.RooStats.PValueToSignificance( 0.05 ),
        "CLsexp": ROOT.RooStats.PValueToSignificance( 0.05 ),
        "clsu1s": ROOT.RooStats.PValueToSignificance( 0.05 ),
        "clsu2s": ROOT.RooStats.PValueToSignificance( 0.05 ),
        "clsd1s": ROOT.RooStats.PValueToSignificance( 0.05 ),
        "clsd2s": ROOT.RooStats.PValueToSignificance( 0.05 ),
      }
    mydict[(x+5,x)] = {
        "CLs":    ROOT.RooStats.PValueToSignificance( 0.01 ),
        "CLsexp": ROOT.RooStats.PValueToSignificance( 0.01 ),
        "clsu1s": ROOT.RooStats.PValueToSignificance( 0.01 ),
        "clsu2s": ROOT.RooStats.PValueToSignificance( 0.01 ),
        "clsd1s": ROOT.RooStats.PValueToSignificance( 0.01 ),
        "clsd2s": ROOT.RooStats.PValueToSignificance( 0.01 ),
      }
    mydict[(x,x/2.)] = {
        "CLs":    ROOT.RooStats.PValueToSignificance( 0.01 ),
        "CLsexp": ROOT.RooStats.PValueToSignificance( 0.01 ),
        "clsu1s": ROOT.RooStats.PValueToSignificance( 0.01 ),
        "clsu2s": ROOT.RooStats.PValueToSignificance( 0.01 ),
        "clsd1s": ROOT.RooStats.PValueToSignificance( 0.01 ),
        "clsd2s": ROOT.RooStats.PValueToSignificance( 0.01 ),
      }
    mydict[(x,0)] = {
        "CLs":    ROOT.RooStats.PValueToSignificance( 0.01 ),
        "CLsexp": ROOT.RooStats.PValueToSignificance( 0.01 ),
        "clsu1s": ROOT.RooStats.PValueToSignificance( 0.01 ),
        "clsu2s": ROOT.RooStats.PValueToSignificance( 0.01 ),
        "clsd1s": ROOT.RooStats.PValueToSignificance( 0.01 ),
        "clsd2s": ROOT.RooStats.PValueToSignificance( 0.01 ),
      }

  # for x in np.linspace( 0, 400, 50 ):
  #   mydict[(x,x/2.)] = {
  #       "CLs":    ROOT.RooStats.PValueToSignificance( 0.01 ),
  #       "CLsexp": ROOT.RooStats.PValueToSignificance( 0.01 ),
  #       "clsu1s": ROOT.RooStats.PValueToSignificance( 0.01 ),
  #       "clsu2s": ROOT.RooStats.PValueToSignificance( 0.01 ),
  #       "clsd1s": ROOT.RooStats.PValueToSignificance( 0.01 ),
  #       "clsd2s": ROOT.RooStats.PValueToSignificance( 0.01 ),
  #     }

  for x in [300,325,350]:
    for y in [0,50,100,150,200]:
      mydict[(x,y)] = {
            "CLs":    ROOT.RooStats.PValueToSignificance( 0.05 ),
            "CLsexp": ROOT.RooStats.PValueToSignificance( 0.05 ),
            "clsu1s": ROOT.RooStats.PValueToSignificance( 0.01 ),
            "clsu2s": ROOT.RooStats.PValueToSignificance( 0.01 ),
            "clsd1s": ROOT.RooStats.PValueToSignificance( 0.05 ),
            "clsd2s": ROOT.RooStats.PValueToSignificance( 0.05 ),
          }


  # for x in np.linspace( 0, 500, 50 ):
  #   mydict[(x+50,x)] = {
  #       "CLs":    2,
  #       "CLsexp": 2,
  #       "clsu1s": 2,
  #       "clsu2s": 2,
  #       "clsd1s": 2,
  #       "clsd2s": 2,
  #     }


  if maxyvalue:
    for x in np.linspace( 0, 2000, 100 ):
      mydict[(x,maxyvalue)] = {
          "CLs":    0,
          "CLsexp": 0,
          "clsu1s": 0,
          "clsu2s": 0,
          "clsd1s": 0,
          "clsd2s": 0,
        }


  # return mydict


def interpolateMassPlane(massPlaneDict = {}, interpolationFunction = "linear"):

  massPoints = massPlaneDict.keys()
  massPointsValues = massPlaneDict.values()

  x0 =   list( zip( *massPoints )[0] )
  y0 =   list( zip( *massPoints )[1] )

  canvas = ROOT.TCanvas("c1","c1",800,600);
  h2D    = ROOT.TH2D("h","h",200,0,2000,200,0,2000);

  #print  massPoints;
  #print  massPointsValues;

  zValues = {} # entry x points
  x={} # entry x points
  y={} # entry x points
  for whichEntry in ["CLs","CLsexp","clsu1s","clsu2s","clsd1s","clsd2s"]:
    zValues[whichEntry] = [ tmpEntry[whichEntry] for tmpEntry in massPointsValues]
    x[whichEntry]       = [ a for a in x0 ];
    y[whichEntry]       = [ a for a in y0 ];
    pass;

  # remove inf point in each entry
  for whichEntry in ["CLs","CLsexp","clsu1s","clsu2s","clsd1s","clsd2s"]:

    if np.isinf( zValues[whichEntry]  ).any():
      print "infs in %s!" % whichEntry;
      pass;

    while np.isinf( zValues[whichEntry]  ).any():
      myindex = np.isinf( zValues[whichEntry]  ).tolist().index(True)
      print "remove i=%d x=%d x=%d" % (myindex,x[whichEntry][myindex],y[whichEntry][myindex])
      x[whichEntry].pop(myindex)
      y[whichEntry].pop(myindex)
      zValues[whichEntry].pop(myindex)
      pass;

    if np.isinf( zValues[whichEntry]  ).any():
      print "still infs in %s!" % whichEntry
      pass;

    pass;
 
  # for i in xrange(len(zValues["CLs"]) ):
  #   if i-1 > len(zValues["CLs"]):
  #     break
  #   if np.isinf(zValues["CLs"][i]):
  #     x.pop(i)
  #     y.pop(i)
  #     for k,v in zValues.iteritems():
  #       zValues[k].pop(i)
  #     i = i-1


  # """
  # to check value in zValues
  for whichEntry in ["CLs","CLsexp","clsu1s","clsu2s","clsd1s","clsd2s"]:
    for i in range(len(x[whichEntry])):
      mass1 = x[whichEntry][i];
      mass2 = y[whichEntry][i];
      z = zValues[whichEntry][i];
      print "(%.2f,%.2f)" % (mass1,mass2) , z;
      h2D.SetBinContent(h2D.GetXaxis().FindBin(mass1),h2D.GetYaxis().FindBin(mass2),z);
      pass;
    h2D.Draw("colz");
    canvas.SaveAs("input_harvest_"+whichEntry+".pdf");
    pass;
  # """

  xi = {}
  yi = {}
  zi = {}
  for whichEntry in ["CLs","CLsexp","clsu1s","clsu2s","clsd1s","clsd2s"]:
    print ">>>> Interpolating %s"%whichEntry;
    xArray = np.array(x[whichEntry]);
    yArray = np.array(y[whichEntry]);
    zValuesArray = np.array( zValues[whichEntry] );
 
    # get xi, yi
    xi[whichEntry], yi[whichEntry] = np.linspace(xArray.min(), xArray.max(), 100), np.linspace(yArray.min(), yArray.max(), 100);
    xi[whichEntry], yi[whichEntry] = np.meshgrid(xi[whichEntry], yi[whichEntry]);

    # interpolate and get zi
    print "size of (x,y,z) = (%d,%d,%d)" % (len(x[whichEntry]), len(y[whichEntry]), len(zValues[whichEntry]));
    rbf = LSQ_Rbf(x[whichEntry], y[whichEntry], zValues[whichEntry], function=interpolationFunction);
    print "setting zi";
    zi[whichEntry] = rbf(xi[whichEntry], yi[whichEntry]);
    pass;

  return (xi,yi,zi);
  # return (x,y,zValues)



def getContourPoints(xi,yi,zi,level ):

  c = plt.contour(xi,yi,zi, [level])
  contour = c.collections[0]

  contourList = []

  for i in xrange( len(contour.get_paths() ) ):
    v = contour.get_paths()[i].vertices

    x = v[:,0]
    y = v[:,1]

    contourList.append( (x,y) )

  return contourList



class LSQ_Rbf(scipy.interpolate.Rbf):

    def __init__(self, *args, **kwargs):
        self.xi = np.asarray([np.asarray(a, dtype=float).flatten()
                           for a in args[:-1]])
        self.N = self.xi.shape[-1]
        self.di = np.asarray(args[-1]).flatten()

        if not all([x.size == self.di.size for x in self.xi]):
            raise ValueError("All arrays must be equal length.")

        self.norm = kwargs.pop('norm', self._euclidean_norm)
        r = self._call_norm(self.xi, self.xi)
        self.epsilon = kwargs.pop('epsilon', None)
        if self.epsilon is None:
            self.epsilon = r.mean()
#        self.smooth = kwargs.pop('smooth', 0.0)
        self.smooth = kwargs.pop('smooth', 0.1)
#        self.smooth = kwargs.pop('smooth', 5.)

        self.function = kwargs.pop('function', 'multiquadric')
#        self.function = kwargs.pop('function', 'linear')

        # attach anything left in kwargs to self
        #  for use by any user-callable function or
        #  to save on the object returned.
        for item, value in kwargs.items():
            setattr(self, item, value)

        print "init_function - eye*smooth"
        #print self.smooth, self.function
        self.A = self._init_function(r) - np.eye(self.N)*self.smooth
        # use linalg.lstsq rather than linalg.solve to deal with
        # overdetermined cases
        print "linalg.lstsq"
        self.nodes = np.linalg.lstsq(self.A, self.di)[0]
        print "End of LSQ_Rbf initialization"


if __name__ == "__main__":
  main()
