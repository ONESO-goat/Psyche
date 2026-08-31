#pragma once 

#include <string>
#include <random>
#include <format>
#include <iostream>
#include "../schema/metadata_structs.h"
#include <uuid/uuid.h>

namespace Helpers {

    /* 
        Create an ID for created agent.
    */
    std::string generateId(Group const& type, std::string_view const& requestedBy);


    /* 
    Create an ID for created agent.
    */
    // std::string generateId(Group type, std::string_view const& requestedBy);

    /*
        @who (string)
        is either 'rosa', 'lina', 'general', or the initials of a worker.
     */
    std::string generateAccessKeyLinux(std::string_view const& who);

    /*
     @who (string)
     is either 'rosa', 'lina', 'general', or the initials of a worker.
     */
    // std::string generateAccessKey(std::string_view const& who);

    /*
        Simple error message command. 
    */
    void errorMsg(int tier, std::string_view const& what, std::string_view const& theError);

}