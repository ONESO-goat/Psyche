#pragma once 

#include <chrono>
#include <string>
#include <string_view>
#include <random>
#include <format>
#include <iostream>
#include <cstring>
#include <system_error>
#include "../schema/metadata_structs.h"
#include <uuid/uuid.h>

namespace Helpers {

    /* 
        Create an ID for created agent.
    */
    std::string generateId(Group const& type, std::string_view const& requestedBy);

    bool validateUsername(std::string const& username);


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
    
    std::string hashPassword(std::string const& password);
    bool verify_password(const std::string& password, const std::string& hashed_password);

    /*
        Simple error message command. 
    */
    void errorMsg(int tier, std::string_view const& what, std::string_view const& theError);

    const std::chrono::year_month_day getDate(bool UTC);

}