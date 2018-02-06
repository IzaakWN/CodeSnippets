#include <vector>
#include <iostream>

struct any {
  enum type {Int, Float, String};
  any(int   e) { m_data.INT    = e; m_type = Int;}
  any(float e) { m_data.FLOAT  = e; m_type = Float;}
  any(char* e) { m_data.STRING = e; m_type = String;}
  type get_type() const { return m_type; }
  int get_int() const { return m_data.INT; }
  float get_float() const { return m_data.FLOAT; }
  char* get_string() const { return m_data.STRING; }
private:
  type m_type;
  union {
    int   INT;
    float FLOAT;
    char *STRING;
  } m_data;
};

template <class ...Args>
void foo_imp(const Args&... args)
{
    std::vector<any> vec = {args...};
    for (unsigned i = 0; i < vec.size(); ++i) {
        switch (vec[i].get_type()) {
            case any::Int: std::cout << vec[i].get_int() << '\n'; break;
            case any::Float: std::cout << vec[i].get_float() << '\n'; break;
            case any::String: std::cout << vec[i].get_string() << '\n'; break;
        }
    }
}

template <class ...Args>
void foo(Args... args)
{
    foo_imp(any(args)...);  //pass each arg to any constructor, and call foo_imp with resulting any objects
}

int main()
{
    char s[] = "Hello";
    foo(1, 3.4f, s);
}