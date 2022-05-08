#! /usr/bin/env python3
# Author: Izaak Neutelings (May 2022)
# Description: Get images from website
# Inspiration:
#   https://beautiful-soup-4.readthedocs.io/en/latest/
#   https://stackoverflow.com/questions/51599798/loop-through-webpages-and-download-all-images?rq=1
#   https://stackoverflow.com/questions/54098316/scrape-img-src-under-div-tag-using-beautifulsoup
# Instructions:
#   pip install beautifulsoup4
import os, re
import requests, contextlib
from dateutil import parser as date_parser # for converting datestamps
from bs4 import BeautifulSoup as soup # for scraping webpages
rexp_qid = re.compile(r"questions/(\d+)/([^/?]*)(:?/[^#]*)?(#\d+)?$")
rexp_img = re.compile(r"https://.*\.(je?pg|png|gif)",re.IGNORECASE)


def format_texdoc(code,header="",verb=0):
  """Format LaTeX code into TikZ standalone."""
  tex_cls_art = r"\documentclass{article}"
  tex_cls_tkz = r'\documentclass[tikz]{standalone}'
  tex_pkg_tkz = r"\usepackage{tikz}"
  tex_doc_beg = r"\begin{document}"
  tex_doc_end = r"\end{document}"
  tex_tkz_beg = r"\begin{tikzpicture}"
  tex_tkz_end = r"\end{tikzpicture}"
  code = code.strip() # strip extra spaces, newlines, etc.
  if all(c in code for c in [tex_tkz_beg,tex_tkz_end]): # find TikZ
    if all(c in code for c in [tex_cls_art,tex_pkg_tkz]): # convert article to standalone file
      if verb>=2:
        print(f">>> REPLACING {tex_cls_art} -> {tex_cls_tkz}")
        print(f">>> REMOVING {tex_pkg_tkz}")
      code = code.replace(tex_cls_art,tex_cls_tkz).replace('\n\n'+tex_pkg_tkz,"").replace('\n'+tex_pkg_tkz,"")
  elif not any(c in code for c in [r"\documentclass",tex_doc_beg,tex_doc_end]): # convert snippet to standalone file
    code = f"{tex_cls_tkz}\n{tex_doc_beg}\n{tex_tkz_beg}\n{code}\n{tex_tkz_end}\n{tex_doc_end}"
  if header: # add author, date, and source
    code = header+'\n'+code
  return code
  

@contextlib.contextmanager
def get_SO_posts(url:str,verb=0):
  """Scrape Stack Overfow questions."""
  # e.g. https://tex.stackexchange.com/search?tab=votes&q=user%3a2552%20%5btikz-pgf%5d
  page = soup(requests.get(url).text,'html.parser')
  divs = page.find_all('div',class_="question-summary search-result")
  urls = [ ] # question URLs
  for div in divs:
    if verb>=2:
      print(f">>> {'-'*6} SEARCH RESULT {'-'*60}")
    for link in div.find_all('a',class_="question-hyperlink"):
      if verb>=2:
        print(f">>> FOUND link {link}")
      href = link.get('href',None) # e.g. /questions/9559/drawing-on-an-image-with-tikz/9562?r=SearchResults#9562
      if href:
        url = f"https://tex.stackexchange.com{href}"
        urls.append(url)
  yield urls
  

@contextlib.contextmanager
def get_codes_and_images(url:str,verb=0):
  """Scrape Stack Overfow question for tex code and images."""
  # e.g. https://tex.stackexchange.com/questions/9559/drawing-on-an-image-with-tikz/
  usr  = "/users/2552/jake"
  page = soup(requests.get(url).text,'html.parser')
  divs = page.find_all('div',class_="answercell") #,recursive=False
  texdocs  = [ ] # full LaTeX documents
  texsnips = [ ] # LaTeX snippets
  imgurls  = [ ] # URL of images attached to answer
  for div in divs:
    if not div.find('a',{'href':usr}): continue
    if verb>=1:
      print(f">>> {'-'*6} POST {'-'*50}")
    ansr = div.find('div',class_="s-prose js-post-body")
    if not ansr: continue
    
    # GET DATE for header
    time = div.find('time',{'itemprop':'dateCreated'})
    header = "% Author: Jake"
    if time:
      dtamp = time.get('datetime',None) # e.g. "2011-01-23T18:11:3
      if dtamp:
        dtime = date_parser.parse(dtamp)
        header += dtime.strftime(" (%B %Y)") # e.g. "(January 2011)"
    header += f"\n% Source: {url}"
    
    # GET CODE
    blocks = [b.find('code') for b in ansr.find_all('pre') if b.find('code')]
    if not blocks:
      print(f">>> NO CODE FOUND!")
    for block in blocks:
      #if '\n' not in code: continue
      code = block.get_text()
      isdoc = r'\begin{document}' in code
      ctype = 'code' if isdoc else 'code snippet'
      if verb>=2:
        print(f">>> FOUND {ctype} {code}")
        print(f">>> ADD header {header}")
      elif verb>=1:
        print(f">>> FOUND {ctype}")
      code = format_texdoc(code,header)
      if isdoc:
        texdocs.append(code)
      else:
        texsnips.append(code)
    
    # GET IMAGES
    imgs = ansr.find_all('img')
    for img in imgs:
      imgurl = img.get('src',None)
      if imgurl and rexp_img.match(imgurl):
        if verb>=1:
          print(f">>> FOUND image {imgurl}")
        imgurls.append(imgurl)
      else:
        print(f">>> Did not recognize image: {img}")
  
  yield texdocs, texsnips, imgurls


def scrape_post(url,**kwargs):
  """Scrape Stack Overfow question post, and download tex code and images."""
  dname = kwargs.get('outdir',None) or "data"
  verb  = kwargs.get('verb',  0   )
  #n = 3 #end value
  os.system(f'mkdir -p {dname}') # added for automation purposes, folder can be named anything, as long as the proper name is used when saving below
  #for i in range(n):
  with get_codes_and_images(url,verb=verb) as (texdocs, texsnips, imgs):
    print(f">>> FOUND {len(texdocs)} tex files, {len(texsnips)} snippets, and {len(imgs)} images")
    if len(texdocs)==0:
      print(">>> WARNING! Did not find any tex files...")
    
    # DOWNLOAD IMAGES
    for i, imgurl in enumerate(imgs,1):
      if verb>=1:
        print(f">>> DOWNLOAD {imgurl}")
      match = rexp_img.match(imgurl)
      ext = match.group(1).lower()
      with open(f'{dname}/image_{i}.{ext}','wb') as file:
        file.write(requests.get(imgurl).content)
    
    # WRITE TEX CODE
    for i, code in enumerate(texdocs,1):
      with open(f'{dname}/code_{i}.tex','w') as file:
        file.write(code)
    
    # WRITE TEX CODE
    for i, code in enumerate(texsnips,1):
      with open(f'{dname}/code_snippet_{i}.tex','w') as file:
        file.write(code)
    

def main(args):
  verb   = args.verb  # verbosity level for debugging
  ipost  =   1        # index of current post
  nposts = args.posts # maximum number of posts to download
  npages = args.pages # maximum number of pages with search results
  searchpage = "https://tex.stackexchange.com/search?tab=votes&q=user%3a2552%20%5btikz-pgf%5d"
  #posts = ["https://tex.stackexchange.com/questions/9559/drawing-on-an-image-with-tikz/",]
  blacklist = ['18389','42401'] # ignore these posts
  for ipage in range(1,npages+1):
    if ipost>nposts: break # limit number of posts
    pageurl = searchpage+(f"&page={ipage}" if ipage>1 else "")
    print(">>>"+"\n>>> "*2)
    print(f">>> # PAGE {ipage}: {pageurl}")
    with get_SO_posts(pageurl,verb=verb) as posts:
      if verb+3>=2:
        print(f">>> FOUND posts:")
        for url in posts: print(f">>>  {url}")
      for url in posts:
        if ipost>nposts: break # limit number of posts
        #print(f">>> FOUND POST {url}")
        match = rexp_qid.search(url)
        print(f">>> ")
        if match:
          qid = match.group(1)
          if qid in blacklist:
            print(f">>> IGNORE blacklisted {url}")
            continue
          qname = match.group(2)
          url = url.replace(match.group(3),'/')
          print(f">>> {'#'*80}")
          print(f">>> # POST {ipost}: {qname}")
          print(f">>> {'#'*80}")
          print(f">>> {url}")
          #print(f">>> ")
          outdir = f"data/question_{ipost:03d}_{qname}" #_{qid}
          scrape_post(url,outdir=outdir,verb=verb)
          ipost += 1
          print(f">>> ")
        else:
          print(f">>> Did not recognize URL for StackOverflow question: {url}")
    print(">>>"+"\n>>> "*2)
    

# QUICK PLOTTING SCRIPT
if __name__ == '__main__':
  from argparse import ArgumentParser
  description = """Download images from web page."""
  parser = ArgumentParser(prog="download_images.py",description=description,epilog="Good luck!")
  parser.add_argument('file', help="final (hadd'ed) ROOT file")
  parser.add_argument('-n','--posts', type=int,default=10,help="maximum number of posts, default=%(default)s")
  parser.add_argument('-p','--pages', type=int,default=1,help="maximum number of pages, default=%(default)s")
  parser.add_argument('-v','--verb',  dest='verbosity',type=int,nargs='?',const=1,default=0,
                                      help="set verbosity")
  args = parser.parse_args()
  main(args)
  
