// #include librerias

// libreria 
#include <iostream>
// libreria standard io(printf..)
#include <stdio.h>

// leer archivos
#include <fstream> // 
#include <iostream>
using namespace std; // para que el codigo vea  cout y endl


int * fibonacci(int num){

    // crear array de tipo int
    int fibonacci[6];

    // asignar valores del array en indices 0 y 1
    fibonacci[0]= 0;
    fibonacci[1]=1;

    for(int i=2;i<6;i++){
        fibonacci[i] = fibonacci[i-1]+fibonacci[i-2];
        i++;
    }

    printf("Terminado!");

    return fibonacci; 
}