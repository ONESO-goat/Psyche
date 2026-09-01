/*
BRAIN

Everything needs a brain to function. 

There are 2 core brains, Generals and LINX.

Generals focus on data, while LINX focus on memory.


*/
#pragma once 

#include <chrono>
#include <tuple>
#include <format>
#include <string>
#include <system_error>
#include <map>
#include <iostream>
#include <string_view>
#include "../schema/metadata_structs.h"


class BrainBase {
protected:

    std::string id;

    /*
        Usally generals should focus on their own fields, weights would be low (< 0.3).
        Linx's will likely be more creative or free on their decisions and new informations.

    */
    float weight;

    /*
        Owner will usually fall in this list: ["ROSA", "GENERAL <name>", "<user's username", "null"|""]
    */
    std::string owner;

     /*
    LINX -> Either user owned or independent
    MANAGER -> LINX's made by generals
    */
    Group groupClass;

    std::unordered_map<std::string, std::string> const character_color;

    std::chrono::year_month_day birthdate;

public:
    /*
        Display brain visualization

        mode (int): 2 = 2D; 3 = 3D

        Default is 2D.
    */
    virtual void showcase(int mode = 2);
    virtual void render_visualize_brain_2D() = 0;  // each subclass implements its own
    virtual void createDatabase() = 0;
    virtual std::unordered_map<std::string, std::any> getBrainData() = 0;
    virtual std::string getId(){return this->id;};
    virtual ~BrainBase() = default;  // virtual destructor, since polymorphic pointers will come eventually
};

class Brain : public BrainBase {
private:


    void render_visualize_brain_2D(
        std::tuple<int,int> figsize, 
        std::string_view border_color, 
        std::string_view _color, 
        std::string_view shape, 
        float Brain_Size
    );

    /*
    LINX -> Either user owned or independent
    MANAGER -> LINX's made by generals
    */
    Group familyClass;

    // example ("john", "", "doe")
    Name first_middle_last_name; 
    std::string id_;

public:
    Brain(
        std::string id_,
        Name const& name, 
        float weight_, 
        Group familyCategory,
        std::string creatorId=""
    );

    /*
    Validate names. First and last names are required, but the middle name is not required. 
    First and last can't be lower than 2 characters, and all can't exceed a length of 100.

    EX; ("john", "", "doe"), ("general", "", "music"), ("jc", "is", "rc")
    */
    bool validateName( Name const& name);

        
    /*
    Show brain with memories represented.
    */
    void render_visualize_brain_2D() override;


    /*
    create database for this 'brain'. The database acts as the "memories" or "knowledge" hoarder 
    rather than just "user password and user description". 

    For now, we can focus on JSON, but SQL or anything more efficient will be the norm later.
    */
    void createDatabase() override;


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
    void forget();

    /*
    LINX feature, LINX's are supposed to be "pets" to users or trusted buddies. Unlike other chatbots
    that are there to answer questions, LINX remembers its user at a deeper scale. To achieve this,
    we'll have to sacrifice knowledge for commitment for the user or its field of knowledge (managers).
    */
    void remember(std::string const& topic);
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

    
    /*
    For linx's, updated data will either be for the user, 
    or new data provided by a General (which means the LINX is a manager).
    LINX's, especially managers will update constantly as new data comes in, out, revised, you name it.
    */
    void update();

    /*
    Primaily General focused, the general searches it's knowledge to come up with a thesis and accurate prediction.
    */
    void search();

    /*
        Get current data like name, id, type, ect...    
    */
    std::unordered_map<std::string, std::any> getBrainData() override;

    std::string getId() override;
};


class GeneralBrain : public BrainBase{
private:

    void render_visualize_brain_2D(
        std::string_view border_color, 
        std::string_view shape, 
        float Brain_Size
        );

    std::string domain;

    Group groupClass = Group::GENERAL;

    // example ("general", "cleaner")
    Name name; 


public:
    GeneralBrain(
    std::string generalId,
    std::string generalDomain,
    float generalWeight,
    std::string creator
    );
    
        
    /*
    Show Data inside the brain. Unlike LINX, here we'll likely use 'matplot' as generals are more focused on data.
    Since generals are pieces of Rosa, this data is technically is a piece of Rosalina's "brain".
    */
    void render_visualize_brain_2D() override;



    /*
    create database for this 'brain'. The database acts as the "memories" or "knowledge" hoarder 
    rather than just "user password and user description". 

    For now, we can focus on JSON, but SQL or anything more efficient will be the norm later.
    */
    void createDatabase() override;


    /*
    Primarily General focused, the general searches 
    it's knowledge to come up with a thesis and accurate prediction.
    */
    void search();

    /*
        Get current data like name, id, type, ect...    
    */
    std::unordered_map<std::string, std::any> getBrainData() override;
};