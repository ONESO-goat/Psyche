#pragma once

#include <string>
#include <unordered_map>
#include <any>
#include <string_view>
#include <optional>


struct Name {
    std::string first, middle, last; 
};

enum class Group {
    USER,
    LINX,
    GENERAL,
    MANAGER
};

namespace SqlFiles {
    constexpr std::string_view users = "user.sql";
    constexpr std::string_view GLINX = "GLINX.sql";
    constexpr std::string_view settings = "settings.sql";
    constexpr std::string_view rosalina = "rosalina.sql";
}

struct User{
    std::string id_;
};

struct LinxAgent{
    std::string brain_id;
    
    std::string id_;
    std::optional<std::string> niche_id;
    Group type;

    Name name;

    float valuation;
    std::string ownerId;
    std::string ownerType;

    std::unordered_map< std::string, std::any> memories;
};



struct GeneralAgent{
    std::string brain_id;
    
    std::string id_;
    std::string niche_id;
    std::string type;
    std::string domain;

    float valuation;

    std::string creatorId;

};


