
#include "helpers.h"
#include "../schema/metadata_structs.h"
#include <sodium.h>


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
        std::string key = std::string(who) + "-";

        while (key.length() < 700) {
            uuid_t raw;
            uuid_generate(raw);

            char uuid[37];
            uuid_unparse(raw, uuid);

            key += uuid;
        }

        key.resize(700);

        return key;
    }


    std::string hashPassword(std::string const& password){
        std::string hashed_password(crypto_pwhash_STRBYTES, password);

        int result = crypto_pwhash_str(
            hashed_password.data(),
            password.c_str(),
            password.length(),
            crypto_pwhash_OPSLIMIT_INTERACTIVE,
            crypto_pwhash_MEMLIMIT_INTERACTIVE
        );

        if (result != 0) {
            throw std::runtime_error("Password hashing failed (out of memory or internal error).");
        }
        hashed_password.resize(std::strlen(hashed_password.c_str()));
        return hashed_password;
    }

    bool verify_password(const std::string& password, const std::string& hashed_password) {
        int result = crypto_pwhash_str_verify(
            hashed_password.c_str(),
            password.c_str(),
            password.length()
        );

        // Returns 0 on successful match, -1 on mismatch
        return result == 0;
    }
    

    /*
        Simple error message command. 
    */
    void errorMsg(int tier, std::string_view const& what, std::string_view const& theError) {
        std::cerr << "[Tier " << tier << "] Error occurred when '" << what << "': " << theError << std::endl;
    }

    const std::chrono::year_month_day getDate(bool UTC=false){
        if (UTC){
            auto now = std::chrono::system_clock::now();
            std::chrono::year_month_day utc_date{std::chrono::floor<std::chrono::days>(now)};
            
            std::cout << "UTC Date: " << utc_date << "\n";
            return utc_date;
        }
        // 1. Get current time point from system clock
        auto now = std::chrono::system_clock::now();

        // 2. Convert system time to local time zone
        auto local_time = std::chrono::current_zone()->to_local(now);

        // 3. Extract the year_month_day date portion
        std::chrono::year_month_day current_date{std::chrono::floor<std::chrono::days>(local_time)};

        return current_date;

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