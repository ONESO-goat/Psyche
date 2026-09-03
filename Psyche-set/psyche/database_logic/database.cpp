/*
database.cpp

Database logic, where we edit sql files, add, remove, etc...
*/


#include "database.h"
#include <fstream>
#include <filesystem>
#include <optional>
#include <ostream>
#include <sstream>


namespace fs = std::filesystem;

Database::Database(std::string const& passkey) : passkey(passkey) {
    if (passkey != "admin123"){std::cerr << "access denied" << std::endl; return;} // passkey hardcoded for now

    if (sqlite3_open("app_data.db", &db) != SQLITE_OK){
        std::cerr << "[DB DEBUG] Failed to open app_data.db: " << sqlite3_errmsg(db) << std::endl;
        Helpers::errorMsg(5, "SQLITE", std::format("Failed to open database: {}", sqlite3_errmsg(db)));
        db = nullptr;
        return;
    }

    sqlite3_exec(db, "PRAGMA foreign_keys = ON;", nullptr, nullptr, nullptr);
    std::cout << "[DB DEBUG] Current working directory: " << fs::current_path() << std::endl;
    thread_local const std::string folderPath = "database_logic/sql_models";
    if (!fs::exists(folderPath)) {
        std::cerr << "[DB DEBUG] ERROR: Directory '" << folderPath 
                  << "' WAS NOT FOUND at " << fs::current_path() << std::endl;
        return;
    }

    int filesProcessed = 0;
    /*
        Looping into sql_models and building each table in each file.
        File system seems to be a file managing tool that will aid with
        checking files, making sure it's the right file, then run.
    */
    if (fs::exists(folderPath) && fs::is_directory(folderPath)){
        for (const auto& entry : fs::directory_iterator(folderPath)){
            if (entry.path().extension() == ".sql"){
                std::cout << "\n[DB DEBUG] Found SQL file: " << entry.path().string() << std::endl;
                std::ifstream file(entry.path());
                if (!file.is_open())
                {
                    Helpers::errorMsg(
                        5, 
                        "File not opening", 
                        std::format(
                            "File '{}' did not open during database creation.\n", 
                            entry.path().stem().string() // get file name without extension attached
                        ) 
                    );
                    continue;
                }
                
                // Reading file content then adding it to a string
                std::stringstream buffer;
                buffer << file.rdbuf();
                const std::string& fileContent = buffer.str();
                if (fileContent.empty()) {
                    std::cerr << "[DB DEBUG] WARNING: File " << entry.path() << " is empty!\n" << std::endl;
                    continue;
                }
                char* errMsg = nullptr;
                // if (sqlite3_exec(db, fileContent.c_str(), nullptr, nullptr, &errMsg) != SQLITE_OK) {
                //     Helpers::errorMsg(5, "SQLITE_INIT", 
                //         std::format("Error running {}: {}", entry.path().string(), errMsg));
                //     sqlite3_free(errMsg);
                // }
                int rc = sqlite3_exec(db, fileContent.c_str(), nullptr, nullptr, &errMsg);
                if (rc != SQLITE_OK) {
                    Helpers::errorMsg(5, "SQLITE_SCHEMA_ERROR", 
                        std::format("Failed executing {}: {}", entry.path().filename().string(), errMsg));
                    sqlite3_free(errMsg);
                } else {
                    std::cout << "[DB DEBUG] Successfully executed: " << entry.path().filename().string() << std::endl;
                    filesProcessed++;
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
    std::optional<std::string> const& nicheId,
    float weight,
    bool _createBrain
) {     
    if (!db) return false;
    (void) reason;

    try {
        
            
        //Group type = std::set<std::string>{"rosa", "lina", "general"}.contains(ownerType) ? Group::MANAGER : Group::LINX;
        
        Group type = ownerType == "general" ? Group::MANAGER : Group::LINX;
        
        std::string const dependency = ownerType.empty() ? "independent" : "dependent";
        std::string const typeString = type == Group::MANAGER ? "manager" : "personal";

        std::string const& id_ = Helpers::generateId(Group::LINX, ownerType);
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
            "INSERT INTO Linx (linx_id, name, {}_id, dependency, niche_id, linx_type) VALUES (?, ?, ?, ?, ?, ?);", 
            ownerType
        );

        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(db, sqlQuery.c_str(), -1, &stmt, nullptr) != SQLITE_OK) {
            Helpers::errorMsg(5, "SQLITE_PREPARE", sqlite3_errmsg(db));
            return false;
        }

        /*
            Setting values to the table after checking security. This can be tedious, so find a way to do this.
        */

        sqlite3_bind_text(stmt, 1, id_.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, fullName.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 3, requestId.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 4, dependency.c_str(), -1, SQLITE_TRANSIENT);
        if (!nicheId.has_value() || nicheId->empty()) {
            sqlite3_bind_null(stmt, 5); // Correctly binds a true SQL NULL
        } else {
            sqlite3_bind_text(stmt, 5, nicheId->c_str(), -1, SQLITE_TRANSIENT);
        }
        sqlite3_bind_text(stmt, 6, typeString.c_str(), -1, SQLITE_TRANSIENT);
        
        // execute
        int rc = sqlite3_step(stmt);
        sqlite3_finalize(stmt);
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

        // TODO: validate username
        

        std::string const id_ = Helpers::generateId(Group::USER, "system");

        const char* sql = "INSERT INTO users (user_id, username, email, password_hash) VALUES (?, ?, ?, ?);";
        sqlite3_stmt* stmt = nullptr;

        if (sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr) != SQLITE_OK){
            Helpers::errorMsg(4, "SQLITE_PREPARE", sqlite3_errmsg(db));
            return false;
        }
        
        sqlite3_bind_text(stmt, 1, id_.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, username.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 3, email.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 4, hashedPassword.c_str(), -1, SQLITE_TRANSIENT);

        // Step and commit changes to the .db file
        int rc = sqlite3_step(stmt);
        sqlite3_finalize(stmt); // Clean up tracking statement

        if (rc != SQLITE_DONE) {
            Helpers::errorMsg(5, "SQLITE_EXECUTE", sqlite3_errmsg(db));
            return false;
        }

        std::cout << "\nUSER ID FOR TESTING: \n\t\u2022" << id_ << std::endl;
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
        std::optional<std::string> const& nicheId,
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

bool Database::does_not_exist(){
    return (!db);
}
