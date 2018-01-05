#define Analyze_cxx
#include "Analyze.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TVirtualPad.h>
#include <TMath.h>

void Analyze::Loop()
{
//   In a ROOT session, you can do:
//      Root > .L Analyze.C
//      Root > Analyze t
//      Root > t.GetEntry(12); // Fill t data members with entry number 12
//      Root > t.Show();       // Show values of entry 12
//      Root > t.Show(16);     // Read and show values of entry 16
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
    
    
    
    // ________ SET-UP ________
    
    TCanvas* lol = new TCanvas("lol","The histograms of Analyze Ville, a happy place to live");
    lol->Divide(2,2,0.01,0.01);
    
    // ebeam histogram
    TH1* ebeamHist = new TH1D("ebeam","Histogram of ebeam",100,149.2,150.8);
    ebeamHist->GetXaxis()->SetTitle("ebeam [GeV]");
    ebeamHist->GetYaxis()->SetTitle("number of events");
    
    // chi2 histogram
    TH1* chi2Hist = new TH1D("chi2","Histogram of chi2",100,0.3,1.7);
    chi2Hist->GetXaxis()->SetTitle("chi2");
    chi2Hist->GetYaxis()->SetTitle("number of events");
    
    // theta histogram
    //TH1* thetaHist = new TH1D("theta","Histogram of Theta",100,0,.240);
    //thetaHist->GetXaxis()->SetTitle("theta [radians]");
    //thetaHist->GetYaxis()->SetTitle("number of events");
    
    // chi2-ebeam histogram
    TH2* cveHist = new TH2D("cve","Scatterplot of chi2 vs. ebeam",100,0.3,1.7,100,149.2,150.8);
                    //  TH2D(name, const char* title,
                    //       Int_t nbinsx, Double_t xlow, Double_t xup,
                    //       Int_t nbinsy, Double_t ylow, Double_t yup)
    cveHist->GetXaxis()->SetTitle("chi2");
    cveHist->GetYaxis()->SetTitle("ebeam [GeV]");
    
    // chi2-theta histogram
    TH2* cvtHist = new TH2D("cvt","Scatterplot of chi2 vs. theta",100,0.3,19,100,-0.005,.3);
                    //  TH2D(name, const char* title,
                    //       Int_t nbinsx, Double_t xlow, Double_t xup,
                    //       Int_t nbinsy, Double_t ylow, Double_t yup)
    cvtHist->GetXaxis()->SetTitle("chi2");
    cvtHist->GetYaxis()->SetTitle("theta [radians]");
    
    
    
    // ________ LOOP ________
    
    Long64_t nentries = fChain->GetEntriesFast();

    Long64_t nbytes = 0, nb = 0;
    for (Long64_t jentry=0; jentry<nentries;jentry++)
    {
        Long64_t ientry = LoadTree(jentry);
        if (ientry < 0) break;
        nb = fChain->GetEntry(jentry);   nbytes += nb;
        // if (Cut(ientry) < 0) continue;
        
        Double_t pt = TMath::Sqrt(px*px + py*py);    // Exercise 5
        Double_t theta = TMath::ATan2(pt,pz);        // Exercise 7
	
        ebeamHist->Fill(ebeam);  // ebeam
        chi2Hist->Fill(chi2);    // chi2
        cveHist->Fill(chi2,ebeam);    // chi2 vs. ebeam
	
        if(chi2<1.5 && theta<0.15)
        {
            cvtHist->Fill(chi2,theta);    // chi2 vs. theta
        }
	
    }
    
    cout << "\n\tHello world! I have a number for you: the last pt=" << pt << "\n" << endl;
    
    
    
    // ________ WRAP-UP ________
    
    // ebeam
    lol->cd(1);
    ebeamHist->Draw("E");
    ebeamHist->Fit("gaus");
    gStyle->SetOptFit();

    // chi2
    lol->cd(2);
    chi2Hist->Draw("E");
    chi2Hist->Fit("gaus");
    gStyle->SetOptFit();
    
    // chi2 vs. ebeam
    lol->cd(3);
    cveHist->Draw();
    
    // chi2 vs. theta
    lol->cd(4);
    cvtHist->Draw();
    
}
