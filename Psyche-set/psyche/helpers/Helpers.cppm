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
};