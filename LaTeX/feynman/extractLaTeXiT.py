#! /usr/bin/env python3
# Author: Izaak Neutelings (August 2024)
# Description: Extract LaTeXiT meta data from image files
# Instructions:
#   python3 -m pip install pypdf    # for PDF
#   python3 -m pip install pillow   # for PNG
#   python3 -m pip install pyobjc   # for using Objective C bindings with LaTeXiT
#   ./extractLaTeXiT.py phi_KK_decay.png
#   ./extractLaTeXiT.py phi_KK_decay.pdf
import os, re
import base64, plistlib, zlib


def getval_from_NSDictionary_deserialized(data,key,verb=0):
  """Retrieve value from deserialized NSDictionary."""
  if verb>=1:
    print(f">>> getval_from_NSDictionary_deserialized: {key!r}")
  idx_top = int(data['$top']['root'])
  idx_key = int(data['$objects'].index(key))-idx_top-1
  idx_val = int(data['$objects'][idx_top]['NS.objects'][idx_key])
  retval  = data['$objects'][idx_val]
  if isinstance(retval,dict) and 'NSString' in retval:
    idx_val = int(retval['NSString'])
    retval = data['$objects'][idx_val]
  return retval
  

def getval_from_NSDictionary(data,key):
  """Retrieve value from NSDictionary."""
  print(f">>> getval_from_NSDictionary: data={data!r}, type(data)={type(data)}")
  retval = str(data[key])[:len(data[key])] # strip attribute
  #retval = re.sub(r"\{\s*NSFont\s*=.+\;\s*\}","",retval) # strip attribute
  return retval
  

def exif2bin(fname,verb=0):
  """Extract binary LaTeXiT metadata from Exif metadata."""
  if verb>=2:
    print(f">>> exif2bin: {fname!r}")
  from PIL import Image
  image = Image.open(fname)
  metakey = 'XML:com.adobe.xmp'
  assert metakey in image.info, f"exif2bin: {fname} does not contain {metakey!r}: {image.info}"
  metadata = image.info['XML:com.adobe.xmp']
  matches = re.findall(r"<exif:UserComment>(.*)</exif:UserComment>",metadata)
  assert matches, f"exif2bin: {fname} does not contain Exif UserComment: {metadata}"
  data_b64 = matches[0]
  data_b64 = data_b64.replace('&#xA;','') # remove HTML new line
  if verb>=2:
    print(f">>> exif2bin: data_b64={data_b64!r}")
  data_bin = base64.b64decode(data_b64)
  if verb>=2:
    print(f">>> exif2bin: data_bin={data_bin!r}")
  return data_bin
  

def exif2meta(fname,verb=0):
  """Extract LaTeXiT metadata from EXIF using zlib & plistlib."""
  if verb>=1:
    print(f">>> exif2meta: {fname!r}")
  data_bin = exif2bin(fname,verb=verb) # load base64 data
  if verb>=2:
    print(f">>> exif2meta: data_bin={data_bin!r}")
  bufsize = int.from_bytes(data_bin[:4],'big') # size in big-endian value
  if verb>=2:
    print(f">>> exif2meta: bufsize={bufsize!r}, data_bin={data_bin!r}")
  data_unz = zlib.decompress(data_bin[4:],bufsize=bufsize)
  data_una = plistlib.loads(data_unz) # unarchive
  print(getval_from_NSDictionary_deserialized(data_una,'preamble'))
  print(getval_from_NSDictionary_deserialized(data_una,'sourceText'))
  

def exif2meta_objc(fname,verb=0):
  """Extract LaTeXiT metadata from PNG using Cocoa / Objective C bindings."""
  if verb>=1:
    print(f">>> exif2meta_objc: {fname!r}")
  import Foundation
  #import Cocoa # alternative to Foundation
  from ctypes import cdll
  cdll.LoadLibrary('/Applications/CODE/TeX/LaTeXiT.app/Contents/MacOS/LaTeXiT')
  data_bin = exif2bin(fname,verb=verb) # load base64 data
  nsdata = Foundation.NSData.dataWithBytes_length_(data_bin,len(data_bin))
  ###nsdata = Foundation.NSData()
  ###nsdata.initWithBase64EncodedString_options_(data_b64,Foundation.NSUTF8StringEncoding)
  nsdata_unz = Foundation.Compressor.zipuncompress_(nsdata)
  data_una = Foundation.NSKeyedUnarchiver.unarchiveObjectWithData_(nsdata_unz)
  if verb>=2:
    print(f">>> exif2meta_objc: data_una={data_una!r}")
  print(getval_from_NSDictionary(data_una,'preamble'))
  print(getval_from_NSDictionary(data_una,'sourceText'))
  

def pdf2meta(fname,verb=0):
  """Extract LaTeXiT metadata from PDF."""
  if verb>=1:
    print(f">>> pdf2meta {fname!r}")
  from pypdf import PdfReader
  reader   = PdfReader(fname)
  metadata = reader.pages[0].extract_text()
  matches  = re.findall(r'<latexit sha1_base64="(.*)">(.*)</latexit>',metadata)
  assert matches, f"pdf2meta: {fname} does not contain LaTeXiT metadata: {metadata}"
  data_b64 = matches[0][1]
  data_bin = base64.b64decode(data_b64)
  bufsize  = int.from_bytes(data_bin[:4],'big') # size in big-endian value
  data_unz = zlib.decompress(data_bin[4:],bufsize=bufsize)
  data_una = plistlib.loads(data_unz) # unarchive
  print(data_una['preamble'])
  print(data_una['source'])
  

def main(args):
  fnames    = args.fnames
  verbosity = args.verbosity
  for fname in fnames:
    if fname.lower().endswith('.pdf'):
      pdf2meta(fname,verb=verbosity)
    else:
      exif2meta(fname,verb=verbosity)
      exif2meta_objc(fname,verb=verbosity)
  

if __name__ == '__main__':
  from argparse import ArgumentParser
  description = '''This script extract fmf.'''
  parser = ArgumentParser(description=description,epilog="Good luck!")
  parser.add_argument('fnames',          nargs='+',
                                         help="input TEX files")
  parser.add_argument('-v', '--verbose', dest='verbosity', type=int, nargs='?', const=1, default=0,
                                         help="set verbosity level" )
  args = parser.parse_args()
  main(args)
  
