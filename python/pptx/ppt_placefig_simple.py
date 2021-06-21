#! /usr/bin/env python
# Author: Izaak Neutelings (June 2021)
# https://towardsdatascience.com/creating-presentations-with-python-3f5737824f61
from __future__ import print_function
from pptx import Presentation
from pptx.util import Cm, Pt
figname1 = "fig/albert.jpg"
figname2 = "fig/curie.jpg"


prs = Presentation()
print(prs)
print("prs.slide_width  = %7r em = %5.2f cm"%(prs.slide_width,prs.slide_width.cm))
print("prs.slide_height = %7r em = %5.2f cm"%(prs.slide_height,prs.slide_height.cm))

# PAGE 1
lyt = prs.slide_layouts[0] # choosing a slide layout
slide1 = prs.slides.add_slide(lyt) # adding a slide
title = slide1.shapes.title # assigning a title
subtitle = slide1.placeholders[1] # placeholder for subtitle
title.text = "Hey, This is a Slide! How exciting!" # title
subtitle.text = "Really?" # subtitle

# PAGE 2
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
fig1 = slide2.shapes.add_picture(figname1,Cm( 3.),Cm(3.),height=Cm(11.)) #,width=Cm(10.))
fig2 = slide2.shapes.add_picture(figname2,Cm(12.),Cm(3.),height=Cm(11.)) #,width=Cm(10.))

prs.save("placefig.pptx") # saving file