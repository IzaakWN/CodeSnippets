// Author: Izaak Neutelings (January 2018)
// Progress bar based on https://stackoverflow.com/a/14539953
//
// g++ -Wall -o progressBar progressBar.cpp
// ./progressBar

#include <iostream>
#include <iomanip> // setw
#include <sstream>
#include <unistd.h> // sleep
#include <string.h>

void progressBar(float progress, int barWidth=50, std::string extramessage=""){
    std::cout << "Progress: [";
    int pos = barWidth * progress;
    for(int i = 0; i < barWidth; ++i){
        if(i < pos) std::cout << "=";
        else if(i==pos) std::cout << ">";
        else std::cout << " ";
    }
    std::cout << "] " << std::setw(3) << int(progress * 100.0) << " % " << extramessage << "    \r";
    std::cout.flush();
    if(progress>0.99999999) std::cout << std::endl;
}

void progressBar(int i, int N, int barWidth=50){
    std::stringstream ss; ss << "("<<i<<" of "<<N<<")";
    progressBar(float(i)/N, barWidth, ss.str());
}

int main(){
    int i0 = 0;
    int N  = 17;
    std::cout<<"\nLoop from "<<i0<<" to "<<N<<std::endl;
    for(int i=i0; i<=N; i++){
        progressBar(i,N);
        usleep(300000); // microseconds
        // ...
    }
    std::cout<<"Done.\n"<<std::endl;
    
}
