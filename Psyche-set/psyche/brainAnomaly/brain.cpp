/*
BRAIN

Everything needs a brain to function. 

There are 2 core brains, Generals and LINX.

Generals focus on data, while LINX focus on memory.


*/




#include "../schema/metadata_structs.h"
#include "../brainAnomaly/brain.h"
#include "../helpers/helpers.h"
void BrainBase::showcase(int mode)
{

}

void Brain::render_visualize_brain_2D(
        std::tuple<int,int> figsize, 
        std::string_view border_color, 
        std::string_view _color, 
        std::string_view shape, 
        float Brain_Size
    )
{
                    // TODO
}

Brain::Brain(
        std::string id_,
        Name const& name, 
        float weight_, 
        Group familyCategory,
        std::string creatorId
    )
{
        if (!validateName(name)){
            return;
        }
        id = std::move(id_);
        owner = std::move(creatorId);
        familyClass = familyCategory;
        first_middle_last_name = name;
        weight = weight_;
        birthdate = Helpers::getDate(true);
}


/*
    Validate names. First and last names are required, but the middle name is not required. 
    First and last can't be lower than 2 characters, and all can't exceed a length of 100.

    EX; ("john", "", "doe"), ("general", "", "music"), ("jc", "is", "rc")
*/
bool Brain::validateName( Name const& name){

        constexpr std::string_view special_chars = "~!@#$%^&*()+`={}[]\\:;<>,.?/";


        if (name.first.empty() || name.last.empty()){
            throw std::length_error("First and last name are required");
        }

        if (std::min(name.last.length(), name.first.length()) < 2  || std::max( name.last.length(), name.first.length()) > 100){
            throw std::length_error("First or Last name falls outside the valid length range (2-100).");
        }
        
        if (name.middle.length() > 100){
            throw std::length_error("Middle name falls outside the valid length range (0-100).");
        }
  
        for (char const n : special_chars){
            if (name.first.find(n) != std::string::npos ||
                name.middle.find(n) != std::string::npos ||    
                name.last.find(n) != std::string::npos    
            ){
                throw std::logic_error("Name cannot include special characters");
            }
            continue;

        }
        
        return true;
}

        
/*
    Show brain with memories represented.
*/
void Brain::render_visualize_brain_2D()
        {

            render_visualize_brain_2D(
            {7, 7},
            "black",
            "light_gray",
            "circle",
            1.0f
            );

}



/*
    create database for this 'brain'. The database acts as the "memories" or "knowledge" hoarder 
    rather than just "user password and user description". 

    For now, we can focus on JSON, but SQL or anything more efficient will be the norm later.
*/
void Brain::createDatabase()
{
        // TODO
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
void Brain::forget()
{
    // TODO
}


/*
    LINX feature, LINX's are supposed to be "pets" to users or trusted buddies. Unlike other chatbots
    that are there to answer questions, LINX remembers its user at a deeper scale. To achieve this,
    we'll have to sacrifice knowledge for commitment for the user or its field of knowledge (managers).
*/
void Brain::remember(std::string const& topic){
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
void Brain::update()
{
    // TODO
}

/*
    primarily General focused, the general searches it's knowledge to come up with a thesis and accurate prediction.
*/
void Brain::search()
{
    // TODO
}

/*
    Get brains ID
*/
std::string Brain::getId()
{
    return this->id;
}


std::unordered_map<std::string, std::any> Brain::getBrainData()
{   
    std::unordered_map<std::string, std::any> data;

    data["id"] = id;
    data["weight"] = weight;
    data["owner"] = owner;
    data["birthdate"] = birthdate;

    return data;
}




//================================================= GENERALS =================================================    


void GeneralBrain::render_visualize_brain_2D(
    std::string_view border_color, 
    std::string_view shape, 
    float Brain_Size
)
{
    // TODO
}



GeneralBrain::GeneralBrain(
    std::string generalId,
    std::string generalDomain,
    float generalWeight,
    std::string creator
    )
{
    id = generalId;
    domain = generalDomain;  
    owner = creator;
    weight = generalWeight; 
}
    
        
/*
    Show Data inside the brain. Unlike LINX, here we'll likely use 'matplot' as generals are more focused on data.
    Since generals are pieces of Rosa, this data is technically is a piece of Rosalina's "brain".
*/
void GeneralBrain::render_visualize_brain_2D()
{
    GeneralBrain::render_visualize_brain_2D(
    "black", 
    "circle", 
    1.0
    );

}



/*
    create database for this 'brain'. The database acts as the "memories" or "knowledge" hoarder 
    rather than just "user password and user description". 

    For now, we can focus on JSON, but SQL or anything more efficient will be the norm later.
*/
void GeneralBrain::createDatabase() 
{

}


/*
    Primarily General focused, the general searches 
    it's knowledge to come up with a thesis and accurate prediction.
*/
void GeneralBrain::search()
{
    // TODO
}

std::unordered_map<std::string, std::any> GeneralBrain::getBrainData()
{   
    std::unordered_map<std::string, std::any> data;

    data["id"] = id;
    data["weight"] = weight;
    data["owner"] = owner;
    data["birthdate"] = birthdate;

    return data;
}