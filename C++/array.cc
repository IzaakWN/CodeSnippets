// Author: Izaak Neutelings (November 2016)
//
// compile and run with
//   g++ array.cc -o array
//   ./array

#include <iostream>
using namespace std;

int main() {
	
	int N = 10;
	double array[N];
    
    for(int i=0; i<N; i++){
      array[i] = i;
    }
    
    for(int i=0; i<N; i++){
      std::cout << "  array[" << i << "] = " << array[i] << std::endl;
    }
	
	return 0;
}
