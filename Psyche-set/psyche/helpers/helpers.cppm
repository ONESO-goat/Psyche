module;
#include <string>
#include <random>
#include <format>
#include <iostream>
#include <array>
#include <algorithm>
#include <stduuid/uuid.h>

export module helpers;

export namespace helpers {
public:
    /* 
    Create an ID for created agent.
    */
    std::string generateId(Group type, std::string requestedBy) {
        std::string mark = "-u";
        if (requestedBy == "rosa") { mark = "-r"; }
        else if (requestedBy == "lina") { mark = "-l"; }

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
        if (type == Group::LINX) {
            return format("LINK-{}{}", uuids::to_string(id), mark);
        } else {
            return format("GENERAL-{}{}", uuids::to_string(id), mark);
        }
    }

    /*
     @who (string)
     is either 'rosa', 'lina', 'general', or the initials of a worker.
     */
    std::string generateAccessKey(std::string who) { 
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
            uuids::to_string(i1), uuids::to_string(i2), 
            uuids::to_string(i3), uuids::to_string(i4), uuids::to_string(i5)
        );
    }

    /*
    Simple error message command. 
    */
    void errorMsg(int tier, string what, string theError) {
        cerr << "[Tier " << tier << "] Error occurred when '" << what << "': " << theError << endl;
    }
};