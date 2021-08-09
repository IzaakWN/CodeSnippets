#! /usr/bin/env python
# Author: Izaak Neutelings (February, 2020)
# Sources:
#   https://docs.python.org/3/library/argparse.html#sub-commands
import sys
from argparse import ArgumentParser

parser = ArgumentParser(prog='PROG') #, parents=[parser_common])
parser.add_argument('-m','--main', action='store_true', help='main option')
subparsers = parser.add_subparsers(title="subcommands",dest='subcommand', #required=False,
                                   help='sub-command help') #, description="valid subcommands",

# COMMON
parser_common = ArgumentParser(add_help=False)
parser_common.add_argument('-c','--common', action='store_true', help='common option')
#parser_common.add_argument('runnumber', type=int, default=10, action='store', #nargs='?',
#                                        help="run number" )

# A COMMAND
parser_a = subparsers.add_parser('a', parents=[parser_common], help='a help') #, aliases=['A']
parser_a.add_argument('-b','--bar', type=int, help='bar help')

# B COMMAND
parser_b = subparsers.add_parser('b', parents=[parser_common], help='b help') #, aliases=['B']
parser_b.add_argument('-b','--baz', choices='XYZ', help='baz help')
parser_b.add_argument('-v','--verbose', default=False, action='store_true', help='baz help')

# ABBREVIATIONS
args = sys.argv[1:]
if args:
  if args[0]=='A': args[0] = 'a' # alias
  if args[0]=='B': args[0] = 'b'

#### COMMON ARGUMENTS, no matter the order
###print ">>> pass 0: args =",args
###args = parser.parse_known_args(args)
###print ">>> pass 1: args =",args
###args[1].append(args[0].subcommand)
####args[1].append(str(args[0].runnumber))
###print ">>> pass 2: args =",args
###args = parser.parse_args(args[1],args[0])
####args = parser.parse_args(args=args[1],namespace=args[0])
###print ">>> pass 3: args =",args
args = parser.parse_args(args)

def do_a():
  print ">>> do a..."
  print ">>>  bar    =",args.bar
  
def do_b():
  print ">>> do b..."
  print ">>>  baz    =",args.baz
  
def main():
  print ">>> main()"
  #print ">>>  runnumber =",args.runnumber
  print ">>>  main   =",args.main
  print ">>>  common =",args.common
  if args.subcommand=='a':
    do_a()
  elif args.subcommand=='b':
    do_b()
  
if __name__ == "__main__":
  main()
  print ">>> done"


