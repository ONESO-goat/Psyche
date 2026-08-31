
#include "helpers.h"

#include <format>
#include <iostream>
#include "../schema/metadata_structs.h"
#include <string>
#include <string_view>
#include <uuid/uuid.h>

namespace Helpers {

    /* 
    Create an ID for created agent.
    */
    std::string generateId(Group const& type, std::string_view const& requestedBy) {
        std::string mark = "-u";
        if (requestedBy == "rosa") { mark = "-r"; }
        else if (requestedBy == "lina") { mark = "-l"; }

        uuid_t raw_id;
        uuid_generate(raw_id);

        char id_[37];
        uuid_unparse(raw_id, id_);
        
        if (type == Group::LINX) {
            return std::format("LINX-{}{}", id_, mark);
        } else {
            return std::format("GENERAL-{}{}", id_, mark);
        }
    }

    

    /*
     @who (string)
     is either 'rosa', 'lina', 'general', or the initials of a worker.
     */
    std::string generateAccessKeyLinux(std::string_view const& who) {
        uuid_t r1, r2, r3, r4, r5;
        uuid_generate(r1); uuid_generate(r2); uuid_generate(r3); uuid_generate(r4); uuid_generate(r5);
        char id1[37], id2[37], id3[37], id4[37], id5[37];
        uuid_unparse(r1, id1); uuid_unparse(r2, id2); uuid_unparse(r3, id3); uuid_unparse(r4, id4); uuid_unparse(r5, id5);

        return std::format("{}-{}{}{}{}{}", std::string(who), id1, id2, id3, id4, id5);
    }
    

    /*
        Simple error message command. 
    */
    void errorMsg(int tier, std::string_view const& what, std::string_view const& theError) {
        std::cerr << "[Tier " << tier << "] Error occurred when '" << what << "': " << theError << std::endl;
    }
}


/*

                    END OF FILE HERE. COMMENTS BELOW ARE FOR FUTURE USE CASES IF NEEDED.

*/



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