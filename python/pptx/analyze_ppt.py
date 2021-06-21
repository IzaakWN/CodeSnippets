# Adapted from: https://github.com/chris1610/pbpython/blob/master/code/analyze_ppt.py
# Instructions: python analyze_ppt.py example.pptx output.pptx
"""
See http://pbpython.com/creating-powerpoint.html for details on this script
Requires https://python-pptx.readthedocs.org/en/latest/index.html

Program takes a PowerPoint input file and generates a marked up version that
shows the various layouts and placeholders in the template.
"""
from __future__ import print_function
from pptx import Presentation
import argparse


def parse_args():
  """ Setup the input and output arguments for the script
  Return the parsed input and output files
  """
  parser = argparse.ArgumentParser(description='Analyze powerpoint file structure')
  parser.add_argument('infile',
                      type=argparse.FileType('r'),
                      help='Powerpoint file to be analyzed')
  parser.add_argument('outfile',
                      type=argparse.FileType('w'),
                      help='Output powerpoint')
  return parser.parse_args()
  

def analyze(index,slide):
  print()
  try:
    title = slide.shapes.title
    title.text = "Title for Layout %s"%(index)
    print("Slide %s"%(index))
  except AttributeError:
    print("No Title for Layout %s"%(index))
  # Go through all the placeholders and identify them by index and type
  for shape in slide.placeholders:
    text = ", text=%r"%(shape.text.encode('utf-8')) if hasattr(shape,'text') else ""
    if shape.is_placeholder:
      phf = shape.placeholder_format
      # Do not overwrite the title which is just a special placeholder
      print("Placeholder: %s, name=%r"%(phf.idx,shape.name)+text)
      if 'Title' not in shape.text:
        shape.text = "Placeholder index=%r name=%r"%(phf.idx,shape.name)
    else:
      print("Shape: shape=%s, type=%r, id=%r"%(shape,shape.shape_type,shape.shape_id)+text)
  for shape in slide.shapes:
    text = ", text=%r"%(shape.text.encode('utf-8')) if hasattr(shape,'text') else ""
    #type = shape.auto_shape_type if hasattr(shape,'auto_shape_type') else ""
    print("Shape: name=%r, type=%r, id=%r"%(
      shape.name,shape.shape_type,shape.shape_id)+text)
  

def analyze_ppt(input, output):
  """ Take the input file and analyze the structure.
  The output file contains marked up information to make it easier
  for generating future powerpoint templates.
  """
  prs = Presentation(input)
  
  # Loop through slides and analyze
  print('\n'+'#'*14)
  print("#   SLIDES   #")
  print('#'*14)
  for index, slide in enumerate(prs.slides):
    analyze(index,slide)
  
  # Each powerpoint file has multiple layouts
  # Loop through them all and  see where the various elements are
  print('\n'+'#'*15)
  print("#   LAYOUTS   #")
  print('#'*15)
  for index, _ in enumerate(prs.slide_layouts):
    slide = prs.slides.add_slide(prs.slide_layouts[index])
    analyze(index,slide)
  
  prs.save(output)
  print()
  

if __name__ == "__main__":
  args = parse_args()
  analyze_ppt(args.infile.name, args.outfile.name)
  
