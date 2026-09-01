/*
    If python associations are slow, we'll migrate to c++.

*/


#include <imports.h>
#include <serpapi.hpp>
#include <rapidjson/document.h>

using  namespace std;
class Association{
    /*
    For speed and save time and effort, we'll find associations by using a search engine.
    In the future we'll use AI to split text and find associations that work using confidence. 
    */
private:
    vector<string> memories;

public:
    Association(){}

    tuple<vector<string>, float> findAssociationsByText(string const& text){
        int n = text.length();
        vector<string> textSplit;
        int left = 0; int right = n - 1;
        for (int i = 0; i < n; i++ ){

        }
    }


    tuple<vector<string>, float> findAssociationsByMemory(string const& text){
        int n = text.length();
        vector<string> textSplit;
        int left = 0; int right = n - 1;
        for (int i = 0; i < n; i++ ){

        }
    }
};