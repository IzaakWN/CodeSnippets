#include <iostream>
#include <vector>
using namespace std;

// http://www.cplusplus.com/forum/general/55651/
//
// compile with
//     g++ vectorDerivedClasses.c
// run with
//     ./a.out



class Animal {
    public:
        std::string name;
        Animal(std::string _name) : name(_name) { }
        virtual void SetName(int arg){ name = arg; }
        virtual void makeNoise(){
            std::cout << "nothing...\"" << std::endl;
        }
};



class Dog : public Animal {
    public:
    Dog(std::string _name) : Animal(_name) { }
        virtual void makeNoise(){
            std::cout << "\"Woof!\"" << std::endl;
        }
};



class Cat : public Animal {
    public:
        Cat(std::string _name) : Animal(_name) { }
        virtual void makeNoise(){
            std::cout << "\"Miauw!\"" << std::endl;
        }
};



void loop(vector<Animal*> keeper){
    for( auto const& animal: keeper ){
        std::cout << animal->name << " says "; animal->makeNoise();
    }
}



int main(){
    
    cout << "\n";
    
    vector<Animal*> keeper;
    keeper.push_back(new Animal("Stevie"));
    keeper.push_back(new Cat("Snuggles"));
    keeper.push_back(new Dog("Bobby"));
    
    loop(keeper);
    
    cout << "\n";
    return 0;
}


