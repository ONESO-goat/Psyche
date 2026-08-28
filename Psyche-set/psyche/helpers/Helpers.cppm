module;
#include <string>
#include <random>
#include <format>
#include "uuid.h"


export module Helpers;
export struct Name {string first, middle, last; };

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

        thread_local std::random_device rd;
        thread_local auto seed_data = []() {
            std::array<int, std::mt19937::state_size> arr;
            std::generate(arr.begin(), arr.end(), std::random_device{});
            return arr;
        }();
        thread_local std::seed_seq seq(seed_data.begin(), seed_data.end());
        thread_local std::mt19937 generator(seq);
        thread_local uuids::uuid_random_generator gen(generator);

        uuids::uuid const id = gen();
        if (type == Group::LINX){

            return std::format("LINK-{}{}", to_string(id), mark);
        } else {
            return std::format("GENERAL-{}{}",to_string(id), mark);
        }
    };

    /*
     @who (string)
     is either 'rosa', 'lina', 'general', or the initials of a worker (select few).
     */
    std::string generateAccessKey(std::string who){ 
        
       thread_local std::random_device rd;
        thread_local auto seed_data = []() {
            std::array<int, std::mt19937::state_size> arr;
            std::generate(arr.begin(), arr.end(), std::random_device{});
            return arr;
        }();
        thread_local std::seed_seq seq(seed_data.begin(), seed_data.end());
        thread_local std::mt19937 generator(seq);
        thread_local uuids::uuid_random_generator gen(generator);

        uuids::uuid const i1 = gen();
        uuids::uuid const i2 = gen();
        uuids::uuid const i3 = gen();
        uuids::uuid const i4 = gen();
        uuids::uuid const i5 = gen();

        return std::format(
            "{}-{}{}{}{}{}", 
            who, 
            to_string(i1), to_string(i2), to_string(i3), to_string(i4), to_string(i5));
        
    };


    /*
    Simple error message command. 
    This is to avoid typing the same thing, where I could forget to add import details.
    */
    void errorMsg(int tier, string what, string theError){
        cerr << "[Tier " << tier << "] Error occurred when '" << what << "': " << theError << endl;
    }
};