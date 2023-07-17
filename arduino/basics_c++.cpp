// #include librerias

// libreria 
#include <iostream>
// libreria standard io(printf..)
#include <stdio.h>

// leer archivos
#include <fstream> // 
#include <iostream>

using namespace std; // para que el codigo vea  cout y endl


// declarar constantes - sustituye nombre de constante con valor
#define CONSTANT1 10;
#define CONSTANT2 'x';
#define CONSTANT3 "hola";






// declarar variables globales - afuera de cualquier funcion
int x = 10; // 16bits
char letra = 'a'; // 1bit
float the_float = 3.1415; // 64bits
double the_double = 10.12393; // 64-128 bits
int a,b,c,d;
short the_short = 2;
long the_long = 100000000;
bool booleano = true; // 1bit


// funciones
// tipo  nombre(tipo param1,tipo param1n){
//    return tipo 
//}

int multiplicar(int x, int y){
    return x*y;
}

    // estructuras/struct (similar a clases- dict)

        // struct nombre{
        //    atributos
        // }; punto y coma

    struct database{
        
        // atributos de estructura
        int id;
        int edad;
        float salario;

    };// 

    // funcion de tipo struct(database)
    database fn(){

        database empleados1;
        empleados1.edad = 30;
        empleados1.id = 1;
        empleados1.salario = 200.123;

        return empleados1;
    }


// funcion main-loop
int main()
{
    // printf: para imprimir (Python print() - Java System.out.println() )
    printf("Hello World!");
    printf("\n");

    // extern tipo:  llamar variables globales   
    


    int edad;
    // input usuario: asignacion de variables externas
    cout<<"Introducir edad: ";
    cin>> edad;
    cin.ignore();

    // condicionales if,else if, else
    if(edad<10){
        printf("Eres un nino!");
    }
    else if(10<=edad && edad<20){

        printf("Eres un adolescente!");
    }
    else if(20<=edad && edad<40){
        printf("Eres un adulto");
    }
    else{

        printf("Ya eres viejito!");
    }
    printf("\n");
    


    // loops

    // for: recorre un array de objetos(int)
    // itera i, de 0-10
    for(int i=0;i<10;i++){

        // imprime int i
        cout<<i<<endl;

    }
    printf("\n");
    
    // while: repite el loop, mientras se cumpla la condicion

    int i = 0;
    // condicion i<10
    while(i<10){
        // imprimir int i en consola
        cout<<i<<endl;
        // aumenta i = i+1 
        i++;

    }

    // do-while: repetir loop al menos una vez (while inverso)
    int x;
    x = 0;

    // action(loop) do - se ejecuta al menos una vez
    do{

        cout<<"Hello world! \n";
        x++;
    }
    // condicion del do(action)
    while(x<5);


    int numA;
    int numB;

    cout<<"Introducir numero A para multiplicar: ";
    cin>> numA;
    cout<<"Introducir numero B para multiplicar: ";
    cin>> numB;
    
    // funcion multiplicar
    c = multiplicar(numA,numB);
    printf("El valor de C es: ");
    cout<<c;
    printf("\n");

    int a;
    cout<<"Introducir numero x: ";
    cin>> a;

    switch(a){
        case 0:{
        printf("Es numero es el 0!");
        break;
        }
        case 1:{
        printf("Es numero es el 1!");
        break;
        }
        default:{
        printf("No es ni 0 ni 1!");
        break;
        }

    }


    int f = 10;
    while(f>5){
        // imprimir int i en consola
        cout<<f<<endl;
        // disminuye i = i+1 
        f--;
        if(f<7){
            printf("break es sacar de la estructura del loop!");
            break;
        }
    }

    int g = 0;
    while(g<10){

        // imprimir int g en consola
        cout<<g<<endl;
        // aumenta g = g+1 
        g++;
        if(g==5||g==7){
            printf("El continue salta a la siguiente iteracion del loop");
            continue;
        }

    }

    
    // pointers: direccion de variables

    int *points_integer; 

    // int normal
    int z;

    // pointer a un integer
    int *p;


    // asignar la dirección de x a p
    p = &x;

    // input de entrada x
    cin>>x;

    cin.ignore();

    // returns direccion de x, en el pointer p
    cout<< *p<<"\n";
    cin.get();

    // inicializar new pointer tipo int
    int *pointer = new int;

    delete pointer;


    // estructuras/struct
    // crear struct tipo database
    database empleados;
    
    // asignar atributos
    empleados.edad = 22;
    empleados.id = 1;
    empleados.salario = 100.100;

    // arrays (lists)

    int int_array[5]; //indice empieza en 0 
    char char_array[5];
    int matriz[5][5];

    int_array[0] = 0;
    char_array[0] ='a';
    matriz[0][0] = 1; 

    // strings data structure 

    string text = "hola";
    char text_char[50];

    // leer archivos
    // crear instancia de ofstream, abre archivo por parametro
    ofstream archivo_w("example.txt");

    // escribe sobre la instancia de ofstream
    archivo_w<<"escribe esto en el archivo";

    // cierra el archivo
    archivo_w.close();



    // abre el archivo para leer
    ifstream archivo_r("example.txt");
    // lee texto del archivo
    archivo_r>>text;
    // output texto leido
    cout<<text;

    cin.get();



    return 0;
}
