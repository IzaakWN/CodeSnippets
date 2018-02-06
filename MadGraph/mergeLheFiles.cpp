// g++ -Wall -o mergeLheFiles mergeLheFiles.cpp
// ls tempdir/*.lhe > list.txt
// ./mergeLheFiles list.txt

#include <iostream>
#include <iomanip> // setw
#include <sstream>
#include <fstream>
#include <vector>
#include <string.h>
#include <stdio.h>

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

int main(int argc, char** argv){

  std::string line;
  std::string line2;
  char* initialFileName;
  const char* outFileName = "./out.lhe";
  std::vector<char*> fileToAddNames;
  
  /* if(argc < 3)
  {
    std::cout << ">>>splitLheFile.cpp::Usage:   " << argv[0] << "   initialFile.lhe   fileToAdd1.lhe   fileToAdd2.lhe ..." << std::endl;
    return -1;
    }*/
  
  char* fileListName = argv[1];
  if(argc > 2)
    outFileName = argv[2];
  if(strcmp(outFileName + strlen(outFileName)-4,".lhe")!=0){
    const char* ext = ".lhe";
    char result[100];
    strcpy(result,outFileName);
    strcat(result,ext);
    outFileName = result;
  }
  
  std::ifstream fileList(fileListName, std::ios::in);
  int fileIt = 0;
  while(!fileList.eof()){
    getline(fileList, line);
    if( !fileList.good() ) break;
    
    char *cline = new char[line.length()+1];
    strcpy(cline, line.c_str());
    
    if(strcmp(cline,outFileName)==0){
      std::cout << "WARNING! Output file "<<outFileName<<" is in list! Ignoring..." << std::endl;
      continue;
    }
    
    if(fileIt==0){
      initialFileName = cline;
      std::cout << "initialFileName = " << initialFileName << std::endl;
    }else{
      fileToAddNames.push_back( cline );
      std::cout << "fileToAddName = " << fileToAddNames.at(fileIt-1) << std::endl;
    }
    fileIt++;
  }

  std::cout << "outFileName = " << outFileName << std::endl;
  std::cout << "Merging " << fileIt << " LHE files" << std::endl;
  /* char* initialFileName = argv[1]; 
  std::cout << "initialFileName = " << initialFileName << std::endl;
  
  std::vector<char*> fileToAddNames;
  for(int fileIt = 0; fileIt < argc-2; ++fileIt)
  {
    fileToAddNames.push_back( argv[2+fileIt] );
    std::cout << "fileToAddName = " << fileToAddNames.at(fileIt) << std::endl;
    }  */
  
  // open lhe file
  std::ifstream initialFile(initialFileName, std::ios::in);
  std::ofstream outFile(outFileName, std::ios::out);
  
  bool writeEvent = false;
  int eventIt = 0;
  
  while(!initialFile.eof()){
  
    progressBar(1,fileIt);
    getline(initialFile, line);
    if( !initialFile.good() ) break;
    if( line == "<event>" ) ++eventIt;
    
    if( line == "</LesHouchesEvents>" ){
      for(int fileIt2 = 0; fileIt2 < fileIt-1; ++fileIt2){
        progressBar(fileIt2+2,fileIt);
        std::ifstream fileToAdd(fileToAddNames.at(fileIt2), std::ios::in);
        
        while(!fileToAdd.eof()){
          getline(fileToAdd, line2); 
          
          // decide whether to skip event or not 
          if( line2 == "<event>" ){
            ++eventIt;
            writeEvent = true;
          }
          
          // write line to outFile
          if(writeEvent == true)
            outFile << line2 << std::endl;
          
          // end of event
          if(line2 == "</event>")
            writeEvent = false;
        }
      }
      break;
    }
    else outFile << line << std::endl;
    
  }
  //progressBar(fileIt,fileIt);
  outFile << "</LesHouchesEvents>" << std::endl;
  
  //std::cout << "Added " << eventIt << " events from " << fileIt-1 << " files to file " << initialFileName << std::endl;
  std::cout << "Added " << eventIt << " events from " << fileIt << " files to file " << outFileName << std::endl;
  return 0;
}
