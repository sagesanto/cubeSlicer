import os
from astropy.io import fits
import shutil
import argparse

def isFits(filePath):
    return filePath[-4:] == ".fit" or filePath[-4:] == "fits"

parser = argparse.ArgumentParser(description='Slice a provided FITS cube into its frames')
parser.add_argument('cubePath', type=str,
                    help='path to the cube to be sliced')
parser.add_argument('outputDir', type=str,
                    help='path to the output directory to store sliced images')
parser.add_argument('-v', '-verbose', action='store_true', dest="verbose", help='enable verbose mode')

args = parser.parse_args()

outputDir = args.outputDir
inputFilename = args.cubePath

if args.verbose:
    print("Reading from",inputFilename,"and outputting to",outputDir)

if not isFits(inputFilename):
    raise ValueError("Provided file must be a .fits or .fit file")

# outputDir = "output/"
if os.path.exists(outputDir):
    shutil.rmtree(outputDir)
os.mkdir(outputDir)

# inputFilename = "../TOI_5671.fits"

file = fits.open(inputFilename)
name = inputFilename.split("/")[-1][:-4]
name = name.replace(".","")
hdu = file[0]
data = hdu.data
header = hdu.header
numSlice = header["NAXIS3"]

if args.verbose:
    print("Slicing the cube into",numSlice,"slices")

for i in range(numSlice):
    if args.verbose:
        print("Slicing frame",i+1)
    newData = data[i,:,:]
    newHeader = header.copy()
    newHeader["NAXIS"] = 2
    del newHeader["NAXIS3"]

    newFITS = fits.PrimaryHDU(newData)
    newFITS.header = newHeader
    outFilename = outputDir+name+"_"+str(i+1)+".fits"
    newFITS.writeto(outFilename)
    if args.verbose:
        print("Sliced and written to",outFilename)

file.close()
if args.verbose:
    print("Slice complete!")