#include <iostream>
#include <math.h>

double MySqrt(int x)
{
    return sqrt(x);
}

int main()
{
    std::cout << "\n\tHello World!";
    std::cout << "\n\tBtw, the sqrt of 4 is " << MySqrt(4) << ".";
    std::cout << "\n\tI know this, because I calculated it with a function.\n\n";
}