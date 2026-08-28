module;
#include <string>
#include <random>
#include <format>
#include "uuid.h"


export module Helpers;

export enum class Group{
    LINX,
    GENERAL,
    MANAGER
};

export enum class SqlFiles{
    users = "user.sql",
    GLINX = "GLINX.sql",
    settings = "settings.sql",
    rosalina = "rosalina.sql"
}

class helpers{
public:
        /* 
        Create a SSN for created agent.
        */
    std::string generateId(Group type, std::string requestedBy){
        std::string mark = "-u";
        if (requestedBy == "rosa"){mark = "-r";}
        else if (requestedBy == "lina"){mark = "-l";}

        std::random_device rd;
        auto seed_data = std::array<int, std::mt19937::state_size>{};

        std::generate(std::begin(seed_data), std::end(seed_data), std::ref(rd));
        std::seed_seq seq(std::begin(seed_data), std::end(seed_data));
        std::mt19937 generator(seq);
        
        uuids::uuid_random_generator gen(generator);

        uuids::uuid const id = gen();
        if (type == Group::LINK){

            return std::format("LINK-{}{}", to_string(id), mark);
        } else {
            return std::format("GENERAL-{}{}",to_string(id), mark);
        }
    };

    /*
    Simple error message command. 
    This is to avoid typing the same thing, where I could forget to add import details.
    */
    void errorMsg(int tier, string what, string theError){
        cout << "[Tier " << tier << "] Error occurred when '" << what << "': " << theError << endl;
    }
};