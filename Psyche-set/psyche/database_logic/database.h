/*
database.cpp

Database logic using SQLite3 for safe, secure, and transactional persistence
*/


#include <format>


#include <chrono>
#include <fstream>
#include <memory>
#include <optional>
#include <set>
#include <string>
#include <string_view>
#include <unordered_map>

#include <sqlite3.h>
#include "../schema/metadata_structs.h"
#include "../brainAnomaly/brain.h"
#include "../helpers/helpers.h"

struct brainParameters{Name name;}; // Add more

using brainResponse = std::optional<std::unique_ptr<LinxAgent>>;

class Database {
private:
    std::string passkey;
    sqlite3* db = nullptr;

public:
    Database(std::string const& passkey); // instructor
    ~Database(); // destructor

    bool linxConnection(
        std::string const& linxId, 
        std::string const& ownerType,
        std::string const& ownerId
    );
   
    bool createLinx(
        std::string const& requestId,
        std::string const& ownerType, 
        std::string reason = "personal", 
        Name const& name = {"linx", "", "Psy"},
        std::optional<std::string> const& nicheId = std::nullopt,
        float weight = 5.0,
        bool _createBrain = false
    );

    bool addUser(
        std::string const& username,
        std::string const& email,
        std::string const& hashedPassword
    );

    /* 
        Access keys are unique keys generals, rosa, or facility have, each unique.
        Basically API keys. If exposed publicly, remove/update it.
    */
    std::string createPrompt(std::string const& accessKey);

    bool validKey(std::string const accessKey);
        // 1: Check if it exists
        // 2. check it's not expired
        // 3. check if the holder exists
        // 4. if a worker, check if its work hours - they can only use it during their work hours
        //  (not needed for now)


    brainResponse InstantiationProtocol(
        std::string const& id_,
        Name const& name,
        Group const& type,
        float const& weight,
        std::optional<std::string> const& nicheId,
        std::string const& requestId,
        std::string const& ownerType

    );

    bool does_not_exist();
};
