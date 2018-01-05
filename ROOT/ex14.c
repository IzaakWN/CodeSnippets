//  Macro created by Izaak Neutelings on 20/03/15.
// Exercise 14:
//      1) Load histograms.
//      2) Get the mean and RMS values of each histogram by fitting a gaussian..
//      3) Make nice log-lin plot with correct title, axis lables, grid, error bars (RMS) etc.
//      4) ???
//      5) Profit.
//


{
    
    #include <sstream> // to loop through hist0..hist5
    
    int n=6;
    
    //TCanvas* c16t = new TCanvas("c16t","Fits");
    //c16t.Divide(2,3,0.001,0.001);
    
    TFile* folders = new TFile("folders.root");
    TDirectory* example1 = folders->GetDirectory("example1");
    example1->cd();
    
    Double_t m[n]; // gaussian mean
    Double_t t[n]; // time
    Double_t e[n]; // error on gaussian mean (RMS)
    
    for (int i=0; i!=n; ++i)
    {
        std::ostringstream os;
        os << "hist" << i;
        TString histiName = os.str();
        
        //c16t.cd(i+1);
        TH1D* histi = gROOT->FindObject(histiName);
        //histi->Draw();
        histi->Fit("gaus");
        fiti = histi->GetFunction("gaus");
        m[i] = fiti->GetParameter(1);
        t[i] = 5*TMath::Power(10,-2+i);
        e[i] = fiti->GetParameter(2);
        
        cout << "\n\tMean = " << m[i] << endl;
        cout << "\tRMS = " << e[i] << "\n" << endl;
    }
    
    TCanvas* c16 = new TCanvas("graph16","Number of charged particles");
    TGraphErrors* graph16 = new TGraphErrors(n,t,m,0,e);
    graph16->Draw("ALP");
    
    graph16->SetTitle("Number of charged atoms in 'Nights in the Gardens of Spain'");
    graph16->GetXaxis()->SetTitle("t [secs]");
    graph16->GetXaxis()->CenterTitle();
    graph16->GetYaxis()->SetTitle("#frac{dn_{ions}}{d(Falla)}");
    graph16->GetYaxis()->CenterTitle();
    graph16->SetMarkerStyle(21);
    c16->SetGrid(1,1);
    c16->SetLogx();
    //c16->Update();
    
}