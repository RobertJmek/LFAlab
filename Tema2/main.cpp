#include <iostream>
#include <fstream>
#include <string>

using namespace std;

ifstream citgr("grammar.txt");
ifstream citcuv("words.txt");
ofstream out("output.txt");

char SimbolCurent;
int NrProd = 0, NrCuv = 0;

class Productions
{
public:
    char NeterminalL;
    char terminal;
    char NeterminalR;
} ProdRules[500];

bool VerifCuv(char *cuvant)
{

    if (cuvant[0] == '\0') // se executa in caz ca am ajuns la final
    {
        if (SimbolCurent == '*')
            return true;

        for (int i = 0; i < NrProd; i++)
        {
            if (ProdRules[i].NeterminalL == SimbolCurent &&
                ProdRules[i].terminal == '*' &&
                ProdRules[i].NeterminalR == '*')
                return true;
        }
        return false;
    }
    else
    { // se continua cu urmatorul subsir din cuvant
        char SmbAux = SimbolCurent;
        for (int i = 0; i < NrProd; i++)
        {
            if (ProdRules[i].NeterminalL == SmbAux &&
                ProdRules[i].terminal == cuvant[0])
            {
                SimbolCurent = ProdRules[i].NeterminalR;
                if (VerifCuv(cuvant + 1))
                    return true;
            }
        }
        return false;
    }
}

int main()
{

    {
        // initiere gramatica(citire)
        citgr >> NrProd;
        for (int i = 0; i < NrProd; i++)
        {
            citgr >> ProdRules[i].NeterminalL;
            citgr >> ProdRules[i].terminal;
            citgr >> ProdRules[i].NeterminalR;
        }
    }

    citcuv >> NrCuv;

    while (NrCuv)
    {
        SimbolCurent = 'S'; // mereu simbolul curent e 'S'
        char *cuv = new char[150];
        citcuv >> cuv;

        if ( VerifCuv(cuv) )
            out << "Cuvantul " << cuv << " este generat de gramatica data.\n";
        else
            out << "Cuvantul " << cuv << " NU este generat de gramatica data.\n";

        delete[] cuv;
        NrCuv--;
    }
}