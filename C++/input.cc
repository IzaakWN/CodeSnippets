// Author: Izaak Neutelings (January 2018)
// Also see: https://www.gnu.org/software/libc/manual/html_node/Getopt.html
//   g++ -Wall -o input input.cc
//   ./input

#include <iostream>
#include <stdio.h>

int main(int argc, char* argv[]){
    
    std::cout << "\n  Receive arguments:" << std::endl;
    std::cout << "    argc = " << argc << std::endl;
    for(int i=0; i<argc; i++)
      std::cout << "    argv[" << i << "] = " << argv[i] << std::endl;
    std::cout << "  Done.\n" << std::endl;
    
    return 0;
}
