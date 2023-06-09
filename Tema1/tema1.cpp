#include <iostream>
#include <fstream>
#include <string.h>
#include <string>
#include <unordered_map>
#include <vector>
#include <algorithm>
using namespace std;

ifstream f("input.txt");

int main()
{
    int nrNoduri;
    f >> nrNoduri;
    int nrNoduriF;
    f >> nrNoduriF;
    vector <int> vectorstari;
    char cuvantdeincercat[100];
    cout<<"Ce cuvant vrei sa incerci? "<<endl;
    cin.get(cuvantdeincercat,100);
    vector<int> VecStFin;
    for (int i = 0; i < nrNoduriF; i++)
    {
        int nod;
        f >> nod;
        VecStFin.push_back(nod);
    }
    
    unordered_map<int, unordered_map<char, int> > sigma;
    int branches = 0;
    f >> branches;
    for (int i = 0; i < branches; i++) {
        int a, b;
        char c;
        f >> a >> c >> b;
        sigma[a][c] = b;
    }

    int currentState = 1;
    for(int i = 0; i < strlen(cuvantdeincercat); i++) {
        char c = cuvantdeincercat[i];
        vectorstari.push_back(currentState);
        if(sigma.find(currentState) == sigma.end()) {
            cout<<"REJECT";
            return 0;
            
        }
        if(sigma[currentState].find(c) == sigma[currentState].end()) {
            cout<<"REJECT";
            return 0;
        
        }
        currentState = sigma[currentState][c];
    }
    if(find(VecStFin.begin(), VecStFin.end(), currentState) != VecStFin.end()) {
        for ( int i=0; i < vectorstari.size(); i++ )
        cout<<vectorstari[i]<<" ";
        cout<<endl;
        cout << "ACCEPT";
        return 0;
    } else {
        cout<< "REJECT";
        return 0;
    }
}