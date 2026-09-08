#pragma once


#include <map>
#include <unordered_map>
#include <string>
#include <iostream>
#include <any>
#include <functional>

#include "../database_logic/database.h"

inline auto& getRosaCalls() {
    thread_local std::unordered_map<std::string, std::function<std::any(std::any, std::any)>> rosaCalls = [] {
        std::unordered_map<std::string, std::function<std::any(std::any, std::any)>> map;
        map["create_general"] = &Database::createGeneral;
        map["create_prompt"] = &Database::createPrompt;
        return map;
    }();
    return rosaCalls;
}