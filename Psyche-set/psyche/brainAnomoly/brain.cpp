/*
BRAIN

Everything needs a brain to function. 

There are 2 core brains, Generals and LINX.

Generals focus on data, while LINX focus on memory.


*/
#include <imports.h>
#include <format>
#include <string_view>

using namespace std;
class Brain{
private:
    /*
        Usally generals should focus on their own fields, weights would be low (< 0.3).
        Linx's will likely be more creative or free on their decisions and new informations.

    */
    float weights;

    /*
    LINX -> Either user owned or independent
    MANAGER -> LINX's made by generals
    */
    Group familyClass;

    // example ("john", "", "doe")
    tuple<string, string, string> first_middle_last_name; 

    /*
        Owner will usually fall in this list: ["ROSA", "GENERAL <name>", "<user's username", "null"|""]
    */
    string owner;

public:
    Brain(
        tuple<string, string, string> const& name, 
        float weight, 
        Group familyCategory,
        string creator=""
    ){
        if (!validateName(name)){
            return;
        }
        owner = creator;
        familyClass = familyCategory;
        first_middle_last_name = name;
        weights = weight;
    }
    /*
    Validate names. First and last names are required, but the middle name is not required. 
    First and last can't be lower than 2 characters, and all can't exceed a length of 100.

    EX; ("john", "", "doe"), ("general", "", "music"), ("jc", "is", "rc")
    */
    bool validateName( tuple<string,string,string> const& name){

        constexpr std::string_view special_chars = "~!@#$%^&*()+`={}[]\\:;<>,.?/";
        
        string first_name = get<0>(name);
        string middle_name = get<1>(name);
        string last_name = get<2>(name);

        if (first_name.empty() || last_name.empty()){
            throw length_error("First and last name are required");
        }

        if (min(last_name.length(), first_name.length()) < 2  || max( last_name.length(), first_name.length()) > 100){
            throw length_error("First or Last name falls outside the valid length range (2-100).");
        }
        
        if (middle_name.length() < 0 || middle_name.length() > 100){
            throw length_error("Middle name falls outside the valid length range (0-100).");
        }
        vector<string> const a = {first_name, middle_name, last_name};
        for (char const n : special_chars){
            if (first_name.find(n) != string::npos ||
                middle_name.find(n) != string::npos ||    
                last_name.find(n) != string::npos    
            ){
                throw logic_error("Name cannot include special characters");
            }
            continue;
        //     int left = 0;
        //     int right = n.size() - 1;
        //     while (left < right)
        //    {     if (special_chars.find(n[right]) != string_view::npos || 
        //             special_chars.find(n[left]) != string_view::npos
        //         ){
        //             throw logic_error("Name cannot include special characters");
        //         }
        //         left++; right--;
        //     }
        }
        
        return true;
    }

    /*
    Display brain visualization

    mode (int): 2 = 2D; 3 = 3D

    Default is 2D.
    */
    void showcase(int mode = 2){

        if (mode == 2){
            render_visualize_brain_2D();
        }
        else if (mode == 3){
            // render_visualize_brain_3D()  // Implement this later
            throw logic_error("3D visual not yet made.");
        }
        else{
            string msg = format("Invalid mode: {}. Choose '2' (for 2D) or '3' (for 3D)", to_string(mode));
            throw logic_error(msg);
        }
    }
        
    /*
    Show brain with memories represented.
    */
    void render_visualize_brain_2D(
                 tuple<int,int> figsize = tuple(7,7), 
                 string border_color="black", 
                 string _color="lightgray", 
                 string shape = "circle", 
                 float Brain_Size= 1.0)
        {

        
        unordered_map<string, string> character_color = {
                {"happy", "yellow"},
                {"sadness", "blue"},
                {"anger", "red"},
                {"fearful", "purple"},
                {"disgusted", "green"},
                {"surprised", "pink"},
                {"neutral", "gray"},
            };

    }



    /*
    create database for this 'brain'. The database acts as the "memories" or "knowledge" hoarder 
    rather than just "user password and user description". 

    For now, we can focus on JSON, but SQL or anything more efficient will be the norm later.
    */
    void createDatabase(){

    }


    /*
        Mainly for LINX, LRU data structure where LINX's forget things if it's not important
        or lacks recurring instances. But, it's not gone forever. We'll save this data to a hoarder 
        that stores old data. Instead of removing it based on time, we'll use math.

        The math considers recent events, user conversation topics, etc.
        EX:
            The user mentioned of a broke up. That'll stick for decades
            The user mentioned phone call of a scammer:
                1st: That stays
                2nd: If anything in the future relates to this scam call, 
                like another one or sterotyping, music, etc, its score is raised and is likely remembered.
            The user mentioned eating pork:
                if the user doesn't face any issue, hardcore event, or importance at the point and time,
                this event is forgotten at a quicker pace.
    */
    void forget(){

    }

    /*
    LINX feature, LINX's are supposed to be "pets" to users or trusted buddies. Unlike other chatbots
    that are there to answer questions, LINX remembers its user at a deeper scale. To achieve this,
    we'll have to sacrifice knowledge for commitment for the user or its field of knowledge (managers).
    */
    void remember(string topic){
        /*
        Here, the flow will likely be we get information, search our database and filter content that fits best.
        Basic RAG, but we'll aim further down memory to achieve either forgotten or special data.

        EX: 
        2 years ago:
                LINX: Get this toy  
                USER: I just got me this new toy and I love it.
        2 days later: 
                USER: Fuck I already broke the toy
        3 years later: 
                LINX: "Remember that time you broke the toy I recommened you and you somehow broke it not even a week in?"
        */

    }
    
    /*
    For linx's, updated data will either be for the user, 
    or new data provided by a General (which means the LINX is a manager).
    LINX's, especially managers will update constantly as new data comes in, out, revised, you name it.
    */
    void update(){

    }

    /*
    Primaily General focused, the general searches it's knowledge to come up with a thesis and accurate prediction.
    */
    void search(){

    }
};


class GeneralBrain{
private:
    /*
        usually generals should focus on their own fields, weights would be low (< 0.3).

    */
    float weight;

    string id;
    string domain;

    Group groupClass = Group::general;

    // example ("general", "cleaner")
    tuple<string, string> name; 

    /*
        Owner will usually fall in this list: ["ROSA","LINA"]
    */
    string owner;

public:
    Brain(
        string generalId,
        string generalDomain, 
        float generalWeight, 
        string creator
    ){
        id = generalId;
        owner = creator;
        familyClass = familyCategory;
        weight = weight;
    }
    
    /*
    Display brain visualization

    mode (int): 2 = 2D; 3 = 3D

    Default is 2D.
    */
    void showcase(int mode = 2){

        if (mode == 2){
            render_visualize_brain_2D();
        }
        else if (mode == 3){
            // render_visualize_brain_3D()  // Implement this later
            throw logic_error("3D visual not yet made.");
        }
        else{
            string msg = format("Invalid mode: {}. Choose '2' (for 2D) or '3' (for 3D)", to_string(mode));
            throw logic_error(msg);
        }
    }
        
    /*
    Show Data inside the brain. Unlike LINX, here we'll likely use 'matplot' as generals are more focused on data.
    Since generals are pieces of Rosa, this data is technically is a piece of Rosalina's "brain".
    */
    void render_visualize_brain_2D(
                 string border_color="black", 
                 string shape = "circle", 
                 float Brain_Size= 1.0
        )
        {


    }



    /*
    create database for this 'brain'. The database acts as the "memories" or "knowledge" hoarder 
    rather than just "user password and user description". 

    For now, we can focus on JSON, but SQL or anything more efficient will be the norm later.
    */
    void createDatabase(){

    }


    /*
    Primarily General focused, the general searches 
    it's knowledge to come up with a thesis and accurate prediction.
    */
    void search(){

    }
};