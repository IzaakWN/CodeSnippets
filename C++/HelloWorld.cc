// Author: Izaak Neutelings (March 2015)
//
// compile and run with
//   g++ HelloWorld.cc
//   ./a.out
// or with:
//   g++ HelloWorld.cc -o HelloWorld
//   ./HelloWorld


#include <iostream>
#include <math.h>

double MySqrt(int x){
    return sqrt(x);
}

int main(){
    std::cout << "\n  Hello World!";
    std::cout << "\n  Btw, the sqrt of 4 is " << MySqrt(4) << ".";
    std::cout << "\n  I know this, because I calculated it with a function.\n\n";
}
