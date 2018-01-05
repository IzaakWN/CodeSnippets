% Hello world!
% This is a test file to test the beheavior of bst files 
% Run this file by creating an test.aux file containing only this line:
%   \bibstyle{test}
% and run in the command line with
%   $ bibtex test.aux
% Ignore these two errors:
%   I found no \citation commands---while reading file min.aux
%   I found no \bibdata command---while reading file min.aux
%
% Read more in this excellent manual "Tame the BeaST":
%   http://www.pirbot.com/mirrors/ctan/info/bibtex/tamethebeast/ttb_en.pdf
%
% Written by Izaak Neutelings, July 2017
%



ENTRY {}{}{}



FUNCTION {helloworld}     %% echo 'Hello World!''
{
  "" top$
  "# Hello World!" top$   %% string is added to stack, and top echoes it
  "" top$
} 



FUNCTION {test1}
{
  "# test1: formatting some names:" top$
  
  "## Steven Weinberg or Weinberg, Steven" top$
  "Steven Weinberg" #1 "{ff }{vv }{ll}" format.name$ top$
  "Steven Weinberg" #1 "{ll, }{vv }{ff, }" format.name$ top$
  "Weinberg, Steven" #1 "{ff }{vv }{ll}" format.name$ top$
  "Weinberg, Steven" #1 "{ll, }{vv }{ff, }" format.name$ top$
  
  "## van der Stenen, Juan" top$
  "van der Stenen, Juan" #1 "{ff }{vv }{ll}" format.name$ top$
  "van der Stenen, Juan" #1 "{ll, }{ff, }{vv}" format.name$ top$
  
  "## {CMS} Collaboration" top$
  "CMS Collaboration" #1 "{ff}" format.name$ top$
  "CMS" #1 "{ff}" format.name$ top$
  "CMS" #1 "{ll}" format.name$ top$
  
  "## {CMS} Collaboration and {ATLAS} Collaboration" top$
  "CMS Collaboration and ATLAS Collaboration" #1 "{ff}" format.name$ top$
  "CMS Collaboration and ATLAS Collaboration" #2 "{ff}" format.name$ top$
  
  "## {CMS} and {ATLAS} Collaboration" top$
  "CMS and ATLAS Collaboration" #1 "{ff}" format.name$ top$
  "CMS and ATLAS Collaboration" #1 "{ll}" format.name$ top$
  "CMS and ATLAS Collaboration" #2 "{ff}" format.name$ top$
  "CMS and ATLAS Collaboration" #2 "{ll}" format.name$ top$

  "" top$
}



STRINGS { arg }                             %% declare string 'arg'
FUNCTION {test2}
{
  "# test2: making variables" top$
  "{CMS} Collaboration" 'arg :=             %% assign string to 'arg'
  arg top$
  arg ", with concatenated string" * top$   %% concatenate
  "" top$
}



FUNCTION {test3_help}                %% pass an argument as 'myarg test3_help'
{
  'arg :=                            %% define 'arg' as the passed argument 
  arg " (passed to test3_help!)" *
}
FUNCTION {test3}
{
  "# test3: passing argument" top$
  "some argument" test3_help top$
  "CMS Collaboration" test3_help top$
  "CMS and ATLAS Collaboration" test3_help top$
  "" top$
}



FUNCTION {test4_help}
{
  'arg :=                            %%               empty$ returns 1 or 0
  arg empty$                         %% if statement; true if expression>0
    { "(empty)" }                    %%   execute this block if true
    { arg #1 "{ff}" format.name$ }   %%   execute this block if false
  if$                                %% end if statement
}
FUNCTION {test4}
{
  "# test4: checking whether it is empty" top$
  "CMS Collaboration" test4_help top$
  "CMS and ATLAS Collaboration" test4_help top$
  "" test4_help top$
  "" top$
}



FUNCTION {test5_help}
{
  'arg :=
  arg empty$
    { "(empty)" }
    { "\textbf{" arg #1 "{ff}" format.name$ * "} Collaboration" * }
  if$
}
FUNCTION {test5}
{
  "# test5: adding word" top$
  "Steven Weinberg" test5_help top$
  "CMS Collaboration" test5_help top$
  "CMS Collaboration and ATLAS Collaboration" test5_help top$
  "CMS and ATLAS Collaboration" test5_help top$
  "" test4_help top$
  "" top$
}


STRINGS { res }
INTEGERS { namei namesleft numnames }        %% declare integers
FUNCTION {test6_loop}
{
  'arg :=
  "" 'res :=                                 %% result string
  #1 'namei :=                               %% namei = 1 (name index)
  arg num.names$ 'numnames :=                %% numnames = number of names in arg
  numnames 'namesleft :=                     %% namesleft = numnames
  { namesleft #0 > }                         %% while namesleft > 0
  {                                          %%
    arg namei "{ff}" format.name$ 'res :=    %%   redefine res
    namei #1 =                               %%   if namei == 1 (first name)
      'res                                   %%     add first name to stack
      {                                      %%
        namesleft #1 =                       %%     if namesleft == 1
          { " and " * res * }                %%       concatenate last string on stack
          { ", " * res * }                   %%       concatenate last string on stack
        if$                                  %%     end if
      }                                      %%
    if$                                      %%   end if
    namei #1 + 'namei :=                     %%   namei     += 1
    namesleft #1 - 'namesleft :=             %%   namesleft -= 1
  }                                          %%
  while$                                     %% close end statement
}
FUNCTION {test6}
{
  "# test6: looping through names, separated by 'and'" top$
  "Steven Weinberg and Richard Feynman and John Anderson" test6_loop top$
  "" top$
}



% Izaak Neutelings, July 2017
% http://www.pirbot.com/mirrors/ctan/info/bibtex/tamethebeast/ttb_en.pdf
% format collaboration fields
%   CMS               -> \textbf{CMS} Collaboration
%   CMS Collaboration -> \textbf{CMS} Collaboration
%   CMS and ATLAS                             -> \textbf{CMS} and \textbf{ATLAS} Collaboration
%   CMS and ATLAS Collaboration               -> \textbf{CMS} and \textbf{ATLAS} Collaboration
%   CMS Collaboration and ATLAS Collaboration -> \textbf{CMS} and \textbf{ATLAS} Collaboration
%   "XENON T100 Collaboration"                -> \textbf{XENON~T100} Collaboration
% Warning! This function abuses format.names's first name {ff} and last name {ll}!
%          This might cause problems with more complicated collaboration names:
%   "XENON T100"               -> \textbf{XENON} Collaboration
% So always end each collaboration name with "Collaboration" in the BibTex field:
%   "XENON T100 Collaboration" -> \textbf{XENON~T100} Collaboration
%   "{XENON~T100}"             -> \textbf{{XENON~T100}} Collaboration
FUNCTION {test7_help}
{
  'arg :=
  "" 'res :=                                     %% result string
  #1 'namei :=                                   %% namei = 1 (name index)
  arg num.names$ 'numnames :=                    %% numnames = number of names in arg
  numnames 'namesleft :=                         %% namesleft = numnames
  { namesleft #0 > }                             %% while namesleft > 0
  {                                              %%
    arg namei "{ff}" format.name$ 'res :=        %%   redefine res using first name {ff}
    res empty$                                   %%   if no match for first name {ff}
      { arg namei "{ll}" format.name$ 'res := }  %%     use last name {ll} instead
      { skip$ }                                  %%     continue
    if$                                          %%   end if
    namei #1 =                                   %%   if namei == 1 (first name)
      { "\textbf{" res * "}" * }                 %%     add first name to stack
      {                                          %%
        namesleft #1 =                           %%     if namesleft == 1
          { " and \textbf{" * res * "}" * }      %%       concatenate last string on stack
          { ", \textbf{" * res * "}" * }         %%       concatenate last string on stack
        if$                                      %%     end if
      }                                          %%
    if$                                          %%   end if
    namei #1 + 'namei :=                         %%   namei     += 1
    namesleft #1 - 'namesleft :=                 %%   namesleft -= 1
  }                                              %%
  while$                                         %% end while
  numnames #1 >                                  %% if names > 1
    { " Collaborations" * }                      %%   add "Collaborations" to last string on stack
    { " Collaboration" * }                       %%   add "Collaboration" to last string on stack
  if$                                            %% end if
}
FUNCTION {test7}
{
  "# test7: my collaboration function" top$
  "CMS" test7_help top$
  "CMS Collaboration" test7_help top$
  "CMS collaboration" test7_help top$
  "CMS and ATLAS" test7_help top$
  "CMS and ATLAS Collaboration" test7_help top$
  "CMS Collaboration and ATLAS Collaboration" test7_help top$
  "XENON T100" test7_help top$                   %% WRONG!
  "{XENON~T100}" test7_help top$                   %% WRONG!
  "XENON T100 Collaboration" test7_help top$
  "" top$
}



READ

EXECUTE{helloworld}
EXECUTE{test1}
EXECUTE{test2}
EXECUTE{test3}
EXECUTE{test4}
EXECUTE{test5}
EXECUTE{test6}
EXECUTE{test7}
