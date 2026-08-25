module;
#include <any>
#include <chrono>
#include <string>
#include <tuple>
#include <unordered_map>

export module structure_mod; 

// Type aliases to make the code readable
using nested_map = std::unordered_map<std::string, std::any>;

export nested_map structure_mod(
    std::tuple<std::string, std::string, std::string> const& name, // Passed by reference for performance
    std::string const& id
) {
    using namespace std::chrono;
    
    auto dp = floor<days>(system_clock::now());
    year_month_day ymd{dp};

    // Explicitly type the sub-maps so std::any knows what they are
    nested_map name_map = {
        {"first_name", std::get<0>(name)},
        {"middle_name", std::get<1>(name)},
        {"last_name", std::get<2>(name)}
    };

    nested_map existence_map = {
        {"creation_date", ymd},
        {"creation_time", dp}
    };

    nested_map brain_map = {
        {"name", name_map}
    };

    nested_map s = {
        {"brain", brain_map},
        {"existence", existence_map},
        {"id", id}
    };

    return s;
}
