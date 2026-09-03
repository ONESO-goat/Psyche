/*
database.cpp

Database logic, where we edit sql files, add, remove, etc...
*/


#include "database.h"
#include <fstream>
#include <filesystem>
#include <sstream>


namespace fs = std::filesystem;

Database::Database(std::string const& passkey) : passkey(passkey) {
    if (passkey != "admin123"){std::cerr << "access denied" << std::endl; return;} // passkey hardcoded for now

    if (sqlite3_open("app_data.db", &db) != SQLITE_OK){
        Helpers::errorMsg(5, "SQLITE", std::format("Failed to open database: {}", sqlite3_errmsg(db)));
        db = nullptr;
        return;
    }

    thread_local const std::string folderPath = "sql_models";

    /*
        Looping into sql_models and building each table in each file.
        File system seems to be a file managing tool that will aid with
        checking files, making sure it's the right file, then run.
    */
    if (fs::exists(folderPath) && fs::is_directory(folderPath)){
        for (const auto& entry : fs::directory_iterator(folderPath)){
            if (entry.path().extension() == ".sql"){
                std::ifstream file(entry.path());
                if (!file.is_open())
                {
                    Helpers::errorMsg(
                        5, 
                        "File not opening", 
                        std::format(
                            "File '{}' did not open during database creation.", 
                            entry.path().stem() // get file name without extension attached
                        ) 
                    );
                    continue;
                }
                
                // Reading file content then adding it to a string
                std::stringstream buffer;
                buffer << file.rdbuf();
                const std::string& fileContent = buffer.str();
                char* errMsg = nullptr;
                if (sqlite3_exec(db, fileContent.c_str(), nullptr, nullptr, &errMsg) != SQLITE_OK) {
                    Helpers::errorMsg(5, "SQLITE_INIT", 
                        std::format("Error running {}: {}", entry.path().string(), errMsg));
                    sqlite3_free(errMsg);
                }
            }
        }
    }
}




Database::~Database() {
    if (db) {
        sqlite3_close(db);
    }
}




bool Database::linxConnection(
    std::string const& linxId, 
    std::string const& ownerType,
    std::string const& ownerId
) {
    if (!db) return false;
    // TODO: not implemented
    std::string command = std::format("select linx where linx_id = {}?", linxId);
    std::unordered_map<std::string, std::string> commands = {
        {"rosa", ""},
        {"user", ""},
        {"general", ""}
    };
    return true;
}
   
bool Database::createLinx(
    std::string const& requestId,
    std::string const& ownerType, 
    std::string reason, 
    Name const& name,
    std::string const& nicheId,
    float weight,
    bool _createBrain
) {     
    if (!db) return false;
    
    try {
        
        std::ofstream sqlFile("sql_models/GLINX.sql", std::ios::app);
        if (!sqlFile.is_open()){
            Helpers::errorMsg(5, "SQL", "GLINX.sql file will not open during linx creation.");
            return false;
        }

            
        Group type = std::set<std::string>{"rosa", "lina", "general"}.contains(ownerType) ? Group::MANAGER : Group::LINX;
        std::string typeString = type == Group::MANAGER ? "manager" : "linx";

        std::string id_ = Helpers::generateId(Group::LINX, ownerType);
        if (id_.empty()){
            Helpers::errorMsg(
                2, 
                "generating ID", 
                std::format("Id returned NULL. Id == {}", id_)
            );
            return false;
        } 
            
        std::string fullName = name.middle != "" ? 
        std::format("{}{}{}", name.first, name.middle, name.last) :
        std::format("{} {}", name.first, name.last);
        

        // Construct query with placeholders. 
        // Note: Column names themselves cannot be parameterized via '?', 
        // but since ownerType is structurally restricted by your system, we can safely string-format it.
        std::string sqlQuery = std::format(
            "INSERT INTO Linx (name, {}_id, niche_id, linx_type) VALUES (?, ?, ?, ?);", 
            ownerType
        );

        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(db, sqlQuery.c_str(), -1, &stmt, nullptr) != SQLITE_OK) {
            Helpers::errorMsg(5, "SQLITE_PREPARE", sqlite3_errmsg(db));
            return false;
        }

        sqlite3_bind_text(stmt, 1, fullName.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, requestId.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 3, nicheId.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 4, typeString.c_str(), -1, SQLITE_TRANSIENT);
        
        // execute
        if (rc != SQLITE_DONE){
            Helpers::errorMsg(5, "SQLITE_EXECUTE", sqlite3_errmsg(db));
            return false;
        }


        if (_createBrain){
                InstantiationProtocol(
                    id_,
                    name,
                    type,
                    weight,
                    nicheId,
                    requestId,
                    ownerType
                );
            }

            return true;

        } catch (const std::runtime_error& ex){
            Helpers::errorMsg(5, "Creating LINX", ex.what());
            return false;
        }
    }

    bool Database::addUser(
        std::string const& username,
        std::string const& email,
        std::string const& hashedPassword
    ) {
        if (!db) return false;
        try {
            // std::ofstream userSqlFile("sql_models/user.sql", std::ios::app);
            // if (!userSqlFile.is_open()) {
            //     Helpers::errorMsg(4, "SQL", "user.sql will not open");
            //     return false;
            // }
        
        const char* sql = "INSERT INTO users (username, email, password) VALUES (?, ?, ?);";
        sqlite3_stmt* stmt = nullptr;

        if (sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr) != SQLITE_OK){
            Helpers::errorMsg(4, "SQLITE_PREPARE", sqlite3_errmsg(db));
            return false;
        }
        
        sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, email.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 3, hashedPassword.c_str(), -1, SQLITE_TRANSIENT);

        // Step and commit changes to the .db file
        int rc = sqlite3_step(stmt);
        sqlite3_finalize(stmt); // Clean up tracking statement

        if (rc != SQLITE_DONE) {
            Helpers::errorMsg(5, "SQLITE_EXECUTE", sqlite3_errmsg(db));
            return false;
        }

        return true;
        }
        catch (const std::runtime_error& ex) {
            Helpers::errorMsg(5, "creating new User", ex.what());
            return false;
        }
    }

    /* 
        Access keys are unique keys generals, rosa, or facility have, each unique.
        Basically API keys. If the key is/was exposed publicly, remove/update it.
    */
    std::string Database::createPrompt(std::string const& accessKey){ 

        if (accessKey.empty() || accessKey.length() != 700){return "invalid key";}
        // TODO: Access key logic here before prompt creation.
        if (!validKey(accessKey)){
            return "invalid key";
        }
        std::string prompt; getline(std::cin, prompt);
        return prompt;
    }

    bool Database::validKey(std::string const accessKey){
        // 1: Check if it exists
        // 2. check it's not expired
        // 3. check if the holder exists
        // 4. if a worker, check if its work hours - they can only use it during their work hours
        //  (not needed for now)

        return false;
    }

    brainResponse Database::InstantiationProtocol(
        std::string const& id_,
        Name const& name,
        Group const& type,
        float const& weight,
        std::string const& nicheId,
        std::string const& requestId,
        std::string const& ownerType

    ){


            /*
                Brains act as physical components for GLINX's.
                Maybe one day get the software into some robots 👀
            */

            auto brain = std::make_unique<Brain>(
                id_, name, weight, type, requestId
            );

            if (!brain || brain == nullptr || brain->getId().empty()){ 
                Helpers::errorMsg(5, "Brain", "The brain wasn't created when making LINX");
                return nullptr;
            }

            std::string brainId = brain->getId();
            auto agent = std::make_unique<LinxAgent>(LinxAgent{
                .brain_id = brainId,
                .id_ = id_,
                .niche_id = nicheId,
                .type = type,
                .name = name,
                .valuation = 0.0f,
                .ownerId = requestId,
                .ownerType = ownerType
            });
            return agent;
        
        }

