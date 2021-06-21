#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Author: Izaak Neutelings (June 2021)
# Instructions for pyhon3:
#   pip3 install python-pptx
#   pip3 install pillow
#   python3 ppt_placefig.py && open placefig.pptx
# Source:
#   https://towardsdatascience.com/creating-presentations-with-python-3f5737824f61
from __future__ import print_function
import os, re
import six, copy
import subprocess
import uuid # for random file names
from math import ceil
from PIL import Image
from pptx import Presentation
from pptx.util import Cm, Pt
from pptx.oxml import parse_xml
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR_TYPE
from pptx.dml.color import RGBColor
from pptx.parts.chart import ChartPart
from pptx.parts.embeddedpackage import EmbeddedXlsxPart
#fileexp = re.compile(r"((?P<file>[^/]+)(?P<ext>\.[a-zA-Z]+))")


def rmslide(pres,i=0):
  """Help function to remove given slide from presentation."""
  del pres.slides._sldIdLst[0]
  

def get_blank_layout(pres,verb=0):
  """Find layout with least amount of items."""
  blank = min(pres.slide_layouts,key=lambda l: len(l.shapes))
  if verb>=1:
    print(">>> get_blank_layout: len(pres.slide_layouts)=%r, index=%d, len(placeholders)=%s, len(shapes)=%s"%(
      len(pres.slide_layouts),pres.slide_layouts.index(blank),len(blank.placeholders),len(blank.shapes)))
  if verb>=2:
    for i, layout in enumerate(pres.slide_layouts):
      print(">>> get_blank_layout: %4d: len(layout)=%d, len(shapes)=%s"%(
        i,len(layout.placeholders),len(layout.shapes)))
      #for placeholder in layout.placeholders: print(placeholder,shape.text)
      #for shape in layout.shapes: print(shape,shape.text if hasattr(shape,'text') else "")
  return blank
  

def duplicate_slide(pres,index=0,verb=0):
  """Duplicate the slide with the given index in pres.
  Adds slide to the end of the presentation"""
  source = pres.slides[index]
  blank_layout = get_blank_layout(pres,verb=verb)
  dest = pres.slides.add_slide(blank_layout)
  ####oldlayout = pres.slide_layouts[pres.slide_layouts.index(source.slide_layout)]
  ###dest = pres.slides.add_slide(oldlayout)
  for shape in source.shapes:
    newel = copy.deepcopy(shape.element)
    dest.shapes._spTree.insert_element_before(newel, 'p:extLst')
  for key, value in source.part.rels.items():
    # Make sure we don't copy a notesSlide relation as that won't exist
    if "notesSlide" not in value.reltype:
      target = value._target
      # if the relationship was a chart, we need to duplicate the embedded chart part and xlsx
      if "chart" in value.reltype:
        partname = target.package.next_partname(
            ChartPart.partname_template)
        xlsx_blob = target.chart_workbook.xlsx_part.blob
        target = ChartPart(partname, target.content_type,
                           copy.deepcopy(target._element), package=target.package)
        target.chart_workbook.xlsx_part = EmbeddedXlsxPart.new(
            xlsx_blob, target.package)
      dest.part.rels.add_relationship(value.reltype,target,value.rId)
  for shape in list(dest.placeholders):
    if not shape.text:
      el = shape.element
      el.getparent().remove(el)
  return dest
  

def pdf2emf(pdffile,tmpdir="",uniq=True,verb=0):
  """Convert PDF to SVG to EMF (PowerPoint or pptx cannot import EPS or PDF)."""
  # If you want to include PDFs. (Might not work for ROOT PDFs)
  # First Install pdf2svg and Inkscape (https://inkscape.org/release/)
  #   ln -s /Applications/Inkscape.app/Contents/MacOS/inkscape /usr/local/bin/inkscape
  #   brew install pdf2svg
  # https://superuser.com/questions/837960/convert-pdf-with-embedded-fonts-to-emf-for-powerpoint
  # https://stackoverflow.com/questions/35367550/convert-svg-pdf-to-emf
  bname, ext = os.path.splitext(os.path.basename(pdffile))
  #assert ext.lower() not in ['.pdf','.svg'], "pdf2emf: Inputfile %s does not have a PDF or SVG extension!"%(pdffile)
  if uniq:
    bname = "%s_%s"%(bname,str(uuid.uuid4().hex)[:8])
  emfname = os.path.join(tmpdir,bname,"_tmp.emf")
  if ext=='.pdf':
    svgfile = os.path.join(tmpdir,bname,"_tmp.svg") # temporary intermediate file
    if verb>=1:
      print(">>> pdf2emf: %s -> %s -> %s"%(pdffile,svgfile,emfname))
    #subprocess.run(["pdf2svg",pdffile,svgfile]) # intermediate 
    #subprocess.run(["inkscape",svgfile,"--export-filename",emfname])
    subprocess.run(["inkscape",pdffile,"--export-filename",emfname,"--pdf-page=1"])
    os.system("rm %s"%(svgfile))
  elif ext=='.svg':
    svgfile = pdffile
    if verb>=1:
      print(">>> pdf2emf: %s -> %s"%(svgfile,emfname))
    subprocess.run(["inkscape",svgfile,"--export-filename",emfname])
    os.system("rm %s"%(svgfile))
  else:
    raise IOError("pdf2emf: Inputfile %s does not have a PDF or SVG extension!"%(pdffile))
  return emfpath
  

def pdf2png(pdffile,dpi=500,tmpdir="",uniq=True,verb=2):
  """Convert PDF to EMF (PowerPoint or pptx cannot import EPS or PDF)."""
  # https://pypi.org/project/pdf2image/
  #   pip install pdf2image
  from pdf2image import convert_from_path
  bname, ext = os.path.splitext(os.path.basename(pdffile))
  assert ext.lower()=='.pdf', "pdf2png: Inputfile %s does not have a PDF extension!"%(pdffile)
  if uniq:
    bname = "%s_%s"%(bname,str(uuid.uuid4().hex)[:8])
  pngfile = os.path.join(tmpdir,bname+".png")
  if verb>=1:
    print(">>> pdf2png: %s -> %s"%(pdffile,pngfile))
  pages = convert_from_path(pdffile,dpi,use_cropbox=True)
  pages[0].save(pngfile,'PNG')
  return pngfile
  

def getfigratio(figname,verb=0):
  """Help function to compute width/height aspect ratio."""
  image  = Image.open(figname)
  width  = image.width #/ image.info['dpi'][0]
  height = image.height #/ image.info['dpi'][1]
  ratio  = width/float(height)
  if verb>=1:
    print(">>> getfigratio: width=%s, height=%s, ratio=%.2f for %r"%(
      image.width,image.height,ratio,figname))
  return ratio
  

def addtext(slide,text,x,y,w,h,**kwargs):
  """Add text (box) to given slide."""
  # https://python-pptx.readthedocs.io/en/latest/api/enum/MsoAutoShapeType.html#msoautoshapetype
  # https://python-pptx.readthedocs.io/en/latest/user/autoshapes.html#adjusting-an-autoshape
  # https://stackoverflow.com/questions/40149992/python-pptx-align-image-to-center-of-slide
  verb    = kwargs.get('verb',   0          )
  tsize   = kwargs.get('lsize',  12         ) # legend font size
  tcolor  = kwargs.get('lcolor', None       ) # legend font color
  fcolor  = kwargs.get('fill',   (6,46,162) ) # box fill color
  lcolor  = kwargs.get('line',   (1,23,81)  ) # box line color 
  thick   = kwargs.get('thick',  1.5        ) # box line thickness (0 = no line)
  bold    = kwargs.get('bold',   True       )
  shadow  = kwargs.get('shadow', False      )
  boxtype = kwargs.get('box',    'round'    )
  print(">>>   Add text at (x,y,w,h)=(%.2f cm,%.2f cm,%.2f cm,%.2f cm): %r"%(x,y,w,h,text))
  const = MSO_SHAPE.ROUNDED_RECTANGLE if 'round' in boxtype else MSO_SHAPE.RECTANGLE
  box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Cm(x),Cm(y),Cm(w),Cm(h))
  box.text = text
  paragraph = box.text_frame.paragraphs[0]
  paragraph.alignment = PP_ALIGN.CENTER
  box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
  box.text_frame.margin_top = 0 #Pt(0.5)
  box.text_frame.margin_bottom = 0 #Pt(0.5)
  if 'round' in boxtype:
    box.adjustments[0] = 0.15 # rounded corner
  ###if not tsize or tsize=='auto':
  ###  #box.text_frame.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
  ###  box.text_frame.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
  ###  #paragraph.font.size = Pt(12)
  ###  box.text_frame.fit_text(font_family='Arial') #autofit_text
  ###else:
  if tsize:
    paragraph.font.size = Pt(tsize)
  if tcolor:
    paragraph.font.color.rgb = RGBColor(*tcolor)
  if bold:
    paragraph.font.bold = True
  box.shadow.inherit = shadow # turn on/off shadow
  fill = box.fill
  if fcolor:
    fill.solid()
    fill.fore_color.rgb = RGBColor(*fcolor)
  else:
    fill.background() # no fill / transparant
  line = box.line
  if thick:
    line.width = Pt(thick)
    if lcolor: # user color
      line.color.rgb = RGBColor(*lcolor)
    #line.color.brightness = 0.5  # 50% lighter
  else:
    line.fill.background() # no line / transparant
  return box
  

def addarrow(slide):
  """Add arrow (in progress)."""
  # ARROW
  connector = slide.shapes.add_shape(MSO_CONNECTOR_TYPE.STRAIGHT,Cm(10.),Cm(5.),Cm(0.),Cm(8.))
  line = connector.line._get_or_add_ln()
  line.append(parse_xml("""
          <a:tailEnd type="arrow" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>
  """))
  return line
  

def addfigslide(pres,title,fignames,positions=[ ],height=0.45,width=None,text="",**kwargs):
  """Add slide with figures."""
  verb    = kwargs.get('verb',    0     ) # level of verbosity
  margins = kwargs.get('margins', (.03,.03,.13,.04) ) # margins for canvas, LRTB
  indices = kwargs.get('order',   None  ) # order of indices to place figures
  reverse = kwargs.get('reverse', False ) # reverse order figures placementx
  nrows   = kwargs.get('nrows',   1     ) # number of figure rows
  ncols   = kwargs.get('ncols',   None  ) # number of figure columns
  tsize   = kwargs.get('tsize',   None  ) # title font size
  dpi     = kwargs.get('dpi',     200   ) # dpi for PDF to PNG conversion
  vector  = kwargs.get('vector',  False ) # convert PDF to EMF vector image (buggy for ROOT PDFs)
  legends = kwargs.get('legends', None  ) # legend (text box) with each figure
  lcoords = kwargs.get('lcoords', (0.60,0.45,0.3,0.1)) # legend coordinates: (xl,yt,w,h)
  slide   = duplicate_slide(pres,0,verb=verb)
  
  # TITLE
  if title:
    slide.shapes.title.text = title
    if tsize:
      slide.shapes.title.text_frame.paragraphs[0].font.size = Pt(tsize)
  
  # CANVAS WIDTH/HEIGHT
  swidth, sheight  = pres.slide_width.cm,  pres.slide_height.cm # slide width, height
  xl, xr = swidth*margins[0], swidth*(1.-margins[1]) # canvas left, right coordinate
  yt, yb = sheight*margins[2], sheight*(1.-margins[3]) # canvas top, bottom coordinate
  cwidth, cheight = xr-xl, yb-yt # canvas width/height
  for figname in fignames:
    assert os.path.isfile(figname), "Filename %r does not exist..."%(figname)
    # TODO: convert PDF to EMF
  if verb>=1:
    print(">>>   swidth=%.2f, sheight=%.2f, title=%r"%(swidth,sheight,title))
    print(">>>   cwidth=%.2f, cheight=%.2f, xl=%.2f, xr=%.2f, yt=%.2f, yb=%.2f"%(
      cwidth,cheight,xl,xr,yt,yb))
  
  # INDICES (order)
  if nrows and not ncols:
    ncols = int(ceil(len(fignames)/float(nrows)))
  elif not nrows and ncols:
    nrows = int(ceil(len(fignames)/float(ncols)))
  if not indices:
    indices = list(range(len(fignames)))
  if reverse: # place figures in reverse
    indices.reverse()
  if verb>=1:
    print(">>>   indices=%s"%(indices))
  
  # CONVERT PDFs (PowerPoint does store PDFs)
  garbage  = set() # remove temporary files at end
  converts = { } # already converted: old -> new
  for i, figname in enumerate(fignames):
    if figname.lower()[-4:] not in [".pdf",".svg"]: continue
    if figname.lower().endswith('.pdf') or figname.lower().endswith('.svg'):
      if figname in converts:
        fignames[i] = converts[figname]
        continue # only convert figure once
      if vector: # vector image: convert PDF to SVG to EMF (buggy in PDFs created by ROOT)
        fignames[i] = pdf2emf(figname,verb=verb)
      else: # bitmap image: convert PDF to PNG
        fignames[i] = pdf2png(figname,dpi=dpi,verb=verb)
      converts[figname] = fignames[i] # old -> new
      garbage.add(fignames[i])
  
  # SET FIGURE WIDTHS/HEIGHTS
  if width:
    fheights = [cheight*height for f in fignames] # figure heights
    fwidths = [cheight*height*getfigratio(f,verb=verb) for f in fignames] # figure widths
  else:
    fheights = [cheight*height for f in fignames] # figure heights
    fwidths = [cheight*height*getfigratio(f,verb=verb) for f in fignames] # figure widths
  if verb>=1:
    print(">>>   fheights=[%s]"%(', '.join("%.3f"%h for h in fheights)))
    print(">>>   fwidths=[%s]"%(', '.join("%.3f"%h for h in fwidths)))
  
  # COMPUTE POSITIONS
  if len(positions)<len(fignames):
    for irow in range(nrows):
      for icol in range(ncols):
        i = irow*ncols+icol
        if i<len(positions): continue # if position already partially filled
        if i>=len(fignames): continue
        w, h = fwidths[i], fheights[i]
        x = xl if icol==0 else xl+icol*cwidth/(ncols-1)-w/2. if icol<(ncols-1) else xr-w
        y = yt if irow==0 else yt+irow*cheight/(nrows-1)-h/2. if irow<(nrows-1) else yb-h
        positions.append((x,y))
        print(">>>   (row,col)=(%d,%d), (x,y)=(%.2f cm,%.2f cm), (w,h)=(%.2f cm,%.2f cm)"%(
          irow,icol,x,y,w,h))
  
  # PLACE FIGURES
  for i in indices:
    if i<0 or i>=len(fignames):
      print(">>>   Warning! Index=%s not valid. len(fignames)=%s Ignoring..."%(i,len(fignames)))
      continue
    figname = fignames[i]
    x, y = positions[i] # figure top left coordinates
    w, h = fwidths[i], fheights[i] # figure width, height
    print(">>>   Add fig %d at (x,y)=(%.2f cm,%.2f cm) from %s"%(i+1,x,y,figname))
    image = slide.shapes.add_picture(figname,Cm(x),Cm(y),height=Cm(h)) #,width=Cm(10.))
    #image.dpi = (10000,10000)
    #image.scale(10,10)
    if legends and 0<=i<len(legends):
      lx, ly = x+lcoords[0]*w, y+lcoords[1]*h
      lw, lh = lcoords[2]*w, lcoords[3]*h
      addtext(slide,legends[i],lx,ly,lw,lh,**kwargs)
  
  #### ARROW
  #### TODO: add arrows per figure
  ###line = addarrow(slide)
  
  # REMOVE INTERMEDIATE FILES
  for fname in garbage:
    if verb>=1:
      print(">>>   Removing temporary file %r..."%(fname))
    os.system("rm %s"%(fname))
  
  return slide
  

def main():
  template  = "templates/UZH_fig.pptx" # template to use for style (incl. footnote, page number, ...)
  outfname  = "placefig.pptx" # output name
  indir     = "fig" # input directory (location of figures)
  years = [ # 1 slide per year
    "2016","2017","2018"
  ]
  vars  = [ # 2x3 variables per slide
    'pt','mvis','njets',
    'pt_logy','mvis_logy','njets_logy',
  ]
  legends   = [ # extra legend (in box) per figure
    "Old", "Old", "Old",
    "New", "New", "New",
  ]
  nrows     = 2 # number of figure rows (2x3=6)
  margins   = (.02,.02,.12,.04) # LRTB margins for canvas
  height    = 0.48 # figure height
  lcoords   = (0.64,0.45,0.23,0.1) # figure legend (text box): x, y, w, h
  verbosity = 1
  
  pres  = Presentation(template)
  for i, year in enumerate(years): # 1 slide per year
    print(">>> Slide %d, %s"%(i,year))
    title = "Some plots for %s, %s"%(i,year)
    fignames = [ ]
    for var in vars: # 6=2x3 variables per slide
      figname = "%s/stack_%s_%s.png"%(indir,var,2018)
      #figname = "%s/stack_%s_%s.pdf"%(indir,var,2018)
      fignames.append(figname)
    addfigslide(pres,title,fignames,height=height,legends=legends,nrows=nrows, #fill=None,thick=None,
                reverse=True,margins=margins,tsize=28,lsize=12,lcoords=lcoords,verb=verbosity)
  rmslide(pres,0) # remove first template slide
  pres.save(outfname) # saving file
  

if __name__ == "__main__":
  main()
  
