#define ex15_cxx
#include "ex15.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TGraphErrors.h>
#include <vector>
#include <sstream> // to loop through hists

void ex15::Loop()
{
//   In a ROOT session, you can do:
//      Root > .L ex15.C
//      Root > ex15 t
//      Root > t.GetEntry(12); // Fill t data members with entry number 12
//      Root > t.Show();       // Show values of entry 12
//      Root > t.Show(15);     // Read and show values of entry 15
//      Root > t.Loop();       // Loop on all entries
//

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
    
    if (fChain == 0) return;
    
    TFile* folders = new TFile("folders.root");
    TDirectory* example2 = folders->GetDirectory("example2");
    example2->cd();
    
    Long64_t nentries = fChain->GetEntriesFast();
    vector<Double_t> m(nentries); // gaussian mean
    vector<Double_t> xVec(nentries); // x
    vector<Double_t> e(nentries); // error on gaussian mean (RMS)
    
    Long64_t nbytes = 0, nb = 0;
    for (Long64_t jentry=0; jentry<nentries; jentry++)
    {
        Long64_t ientry = LoadTree(jentry);
        if (ientry < 0) break;
        nb = fChain->GetEntry(jentry);   nbytes += nb;
        // if (Cut(ientry) < 0) continue;
        
        std::ostringstream os;
        os << "hist" << histNumber;
        TString histName = os.str();
        
        TH1D* hist = (TH1D*) gROOT->FindObject(histName);
        hist->Fit("gaus","0");
        fit = hist->GetFunction("gaus");
        m[ientry] = fit->GetParameter(1);
        xVec[ientry] = x;
        e[ientry] = fit->GetParameter(2);
        
        //cout << "\nientry: " << ientry << " van de " << nentries << endl;
        //cout << "histNumber: " << histNumber << endl;
        //cout << "x = " << x << ", m = " << m[ientry] << endl;
        //cout << "histName: \"" << histName << "\"\n" << endl;

    }
    
    TCanvas* c15 = new TCanvas("graph15","Number of lulz I had");
    TGraphErrors* graph15 = new TGraphErrors(nentries,&xVec[0],&m[0],0,&e[0]);
    graph15->Draw("ALP");
    
    graph15->SetTitle("Number of lulz I had last month");
    graph15->GetXaxis()->SetTitle("x [day]");
    graph15->GetXaxis()->CenterTitle();
    graph15->GetYaxis()->SetTitle("mean of that day");
    graph15->GetYaxis()->CenterTitle();
    graph15->SetMarkerStyle(21);
    c15->SetGrid(1,1);

}


int main(int argc, char **argv)
{
    TApplication theApp("App",&argc,argv);
    ex15 a;
    a.Loop();
    theApp.Run();
    return 0;
}
