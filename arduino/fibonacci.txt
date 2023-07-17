// #include librerias

// libreria 
#include <iostream>
// libreria standard io(printf..)
#include <stdio.h>

// leer archivos
#include <fstream> // 
#include <iostream>
using namespace std; // para que el codigo vea  cout y endl


void fibonacci(int num){

    if(num == 1){
        cout<<0<<endl;
    }

    int n_2 = 0;
    int n_1 = 1;
    int n;
    
    cout<<0<<endl;
    cout<<1<<endl;


    for(int i=3;i<=num;i++){

        n = n_2+n_1;
        cout<<""<<n;
        n_2=n_1;
        n_1=n;
    }
}

int main(){

    int num;
    cout<<"Number of elements of Fibonacci series to generate:";
    cin>>num;

    fibonacci(num);
    return EXIT_SUCCESS;

}