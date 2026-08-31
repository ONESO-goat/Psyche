module;
#include <string>
#include <random>
#include <format>
#include <iostream>
#include "../schema/metadata_structs.h"
#include <uuid/uuid.h>

export module helpers;

export namespace HelpersModule {

    /* 
    Create an ID for created agent.
    */
    inline std::string generateId(Group type, std::string requestedBy) {
        std::string mark = "-u";
        if (requestedBy == "rosa") { mark = "-r"; }
        else if (requestedBy == "lina") { mark = "-l"; }
        uuid_t raw_id;
        uuid_generate(raw_id);
        char id_[37];
        if (type == Group::LINX) {
            return std::format("LINK-{}{}", id_, mark);
        } else {
            return std::format("GENERAL-{}{}", id_, mark);
        }
    }

    /* 
    Create an ID for created agent.
    */
    // std::string generateId(Group type, std::string requestedBy) {
    //     std::string mark = "-u";
    //     if (requestedBy == "rosa") { mark = "-r"; }
    //     else if (requestedBy == "lina") { mark = "-l"; }

    //     thread_local std::random_device rd;
    //     thread_local auto seed_data = []() {
    //         std::array<int, std::mt19937::state_size> arr;
    //         std::generate(arr.begin(), arr.end(), std::random_device{});
    //         return arr;
    //     }();
    //     thread_local std::seed_seq seq(seed_data.begin(), seed_data.end());
    //     thread_local std::mt19937 generator(seq);
    //     thread_local uuids::uuid_random_generator gen(generator);

    //     uuids::uuid const id = gen();
    //     if (type == Group::LINX) {
    //         return std::format("LINK-{}{}", uuids::to_string(id), mark);
    //     } else {
    //         return std::format("GENERAL-{}{}", uuids::to_string(id), mark);
    //     }
    // }

    /*
     @who (string)
     is either 'rosa', 'lina', 'general', or the initials of a worker.
     */
    inline std::string generateAccessKeyLinux(std::string who) {
        uuid_t raw_id;
        uuid_generate(raw_id);
        char id1[37];
        char id2[37];
        char id3[37];
        char id4[37];
        char id5[37];

        uuid_unparse(raw_id, id1);

        return std::format("{}-{}{}{}{}{}", who, id1, id2, id3, id4, id5);
    }
    /*
     @who (string)
     is either 'rosa', 'lina', 'general', or the initials of a worker.
     */
    // std::string generateAccessKey(std::string who) { 
    //     thread_local std::random_device rd;
    //     thread_local auto seed_data = []() {
    //         std::array<int, std::mt19937::state_size> arr;
    //         std::generate(arr.begin(), arr.end(), std::random_device{});
    //         return arr;
    //     }();
    //     thread_local std::seed_seq seq(seed_data.begin(), seed_data.end());
    //     thread_local std::mt19937 generator(seq);
    //     thread_local uuids::uuid_random_generator gen(generator);

    //     uuids::uuid const i1 = gen();
    //     uuids::uuid const i2 = gen();
    //     uuids::uuid const i3 = gen();
    //     uuids::uuid const i4 = gen();
    //     uuids::uuid const i5 = gen();

    //     return std::format(
    //         "{}-{}{}{}{}{}", 
    //         who, 
    //         uuids::to_string(i1), uuids::to_string(i2), 
    //         uuids::to_string(i3), uuids::to_string(i4), uuids::to_string(i5)
    //     );
    // }

    /*
    Simple error message command. 
    */
    inline void errorMsg(int tier, std::string what, std::string theError) {
        std::cerr << "[Tier " << tier << "] Error occurred when '" << what << "': " << theError << std::endl;
    }
};