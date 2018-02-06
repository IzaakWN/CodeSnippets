// Author: Izaak Neutelings (November 2016)
// http://www.cplusplus.com/forum/general/55651/
//
// compile and run with
//   g++ vectorDerivedClasses.c -o vectorDerivedClasses
//   ./vectorDerivedClasses

#include <iostream>
#include <vector>
using namespace std;



class a {
    protected:
        int test;
    public:
        virtual void SetTest(int arg){ test = arg; }
        int GetTest(){ return test; }
};



class b : public a {
    public:
        void SetTest(int arg){ test = arg+1; }
};



class c : public a {
    public:
        void SetTest(int arg){ test = arg+2; }
};



void loop(vector<a*> holder){
    for( auto const& obj: holder ){
        cout << obj->GetTest() << "\n";
    }
}



int main(){
    
    vector<a*> holder;
    holder.push_back(new a);
    holder.push_back(new b);
    holder.push_back(new c);
    
    for(int i = 0; i < (int)holder.size(); i++){
        holder[i]->SetTest(5);
    }
    
    loop(holder);
    
    //for(int i = 0; i < (int) derivedClassHolder.size(); i++){
    //    cout << derivedClassHolder[i]->GetTest() << "  ";
    //}
    
    cout << "\n";
    return 0;
}


