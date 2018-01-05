//  Macro created by Izaak Neutelings on 20/03/15.
//  Exercise 16:
//      1) Load histograms.
//      2) Get the mean and RMS values of each histogram by fitting a gaussian..
//      3) Make nice plot with correct title, axis lables, grid, error bars (RMS) etc.
//      4) ???
//      5) Profit.
//


{
    
    #include <sstream> // to loop through hist0..hist5
    #include <vector>
    
    //TCanvas* c16t = new TCanvas("c16t","Fits");
    //c16t.Divide(2,3,0.001,0.001);
    
    TFile* folders = new TFile("folders.root");
    TDirectory* example3 = folders->GetDirectory("example3");
    //example3->cd();
    
    int n = example3->GetNkeys();
    TIter next(example3->GetListOfKeys());
    TKey* key;
    
    vector<Double_t> m(n); // gaussian mean
    vector<Double_t> x(n); // x
    vector<Double_t> e(n); // error on gaussian mean (RMS)
    
    int i = 1; // count histograms
    int j = 1; // count histograms after cut
    
    while ( ( key = (TKey*) next() ) )
    {
        TString name = key->GetName();
        TString title = key->GetTitle();
        
        cout << "\nKey " << i << endl;
        cout << "   name: " << name << endl;
        cout << "   title: " << title << endl;
        
        ++i;
        
        if ( name->BeginsWith("plotAfter") )
        {
            cout << "   Check; plotAfter, number " << j << endl;
            
            TH1* hist = (TH1*) key->ReadObj();
            hist->Fit("gaus","0");
            fit = hist->GetFunction("gaus");
            m[j] = fit->GetParameter(1);
            e[j] = fit->GetParameter(2);
            x[j] = title->Atof();
            
            ++j;
        }
    }
    
    TCanvas* c16 = new TCanvas("graph16","Number of charged particles");
    TGraphErrors* graph16 = new TGraphErrors(n,&x[0],&m[0],0,&e[0]);
    graph16->Draw("APF");
    
    graph16->SetTitle("Iets");
    graph16->GetXaxis()->SetTitle("x [units]");
    graph16->GetXaxis()->CenterTitle();
    graph16->GetYaxis()->SetTitle("niets");
    graph16->GetYaxis()->CenterTitle();
    graph16->SetMarkerStyle(21);
    c16->SetGrid(1,1);
    //c16->SetLogx();
    //c16->Update();
    
    cout << "\nNumber of plotAfters: " << j << endl;
    cout << "Fin.\n" << endl;
}