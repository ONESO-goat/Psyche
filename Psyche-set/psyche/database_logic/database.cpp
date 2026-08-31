/*
database.cpp

Database logic, where we edit sql files, add, remove, etc...
*/


#include <cstddef>
#include <format>
#include "../helpers/helpers.h"
#include "../helpers/imports.h"
#include <chrono>
#include <fstream>
#include <memory>
#include <optional>
#include <set>
#include <string>
#include <string_view>
#include <unordered_map>
#include "../schema/metadata_structs.h"


struct brainParameters{Name name;}; // Add more

union brainResponse{
    std::unique_ptr<LinxAgent> agent;
    std::nullptr_t noResponse = nullptr;
};

class Database {
private:
    std::string passkey;

public:
    Database(std::string const passkey) : passkey(passkey) {}

    bool linxConnection(
        std::string const& linxId, 
        std::string const& ownerType,
        std::string const& ownerId
    ) {
        // TODO: not implemented
        std::string command = std::format("select linx where linx_id = {}?", linxId);
        std::unordered_map<std::string, std::string> commands = {
            {"rosa", ""},
            {"user", ""},
            {"general", ""}
        };
        return true;
    }
   
    bool createLinx(
        std::string const& requestId,
        std::string const& ownerType, 
        std::string reason = "personal", 
        Name const& name = {"linx", "", "Psy"},
        std::string_view const& nicheId = "",
        float weight = 5.0,
        bool _createBrain = false
    ) {      
        try {
         
            std::fstream sqlFile("sql_models/GLINX.sql", std::ios::app);
            if (!sqlFile.is_open()){
                Helpers::errorMsg(5, "SQL", "GLINX.sql file will not open during linx creation.");
                return false;
            }
            std::string type = std::set<std::string>{"rosa", "lina", "general"}.contains(ownerType) ? "manager" : "personal";
            
            std::string id_ = Helpers::generateId(Group::LINX, ownerType);
            if (id_.empty()){
                std::cerr << Helpers::errorMsg(2, "generating ID", std::format("Id returned NULL. Id == {}", id_)) << endl;
                return false;
            } 
            
            std::string fullName = name.middle != "" ? 
            std::format("{}{}{}", name.first, name.middle, name.last) :
            std::format("{} {}", name.first, name.last);

            std::string command = std::format(
                "insert into Linx\n"
                " (name, {0}_id, niche_id, linx_type)\n"
                " values ('{1}', '{2}', '{3}', '{4}')\n",
                ownerType, fullName, requestId, nicheId, type 
            );
            sqlFile << command;
            sqlFile.close();
            if (_createBrain){
                InstantiationProtocol();
            }

            return true;

        } catch (const std::runtime_error& ex){
            Helpers::errorMsg(5, "Creating LINX", ex.what());
            return false;
        }
    }

    bool addUser(
        std::string const& username,
        std::string const& email,
        std::string const& hashedPassword
    ) {
        try {
            std::fstream userSqlFile("sql_models/user.sql", std::ios::app);
            if (!userSqlFile.is_open()) {
                Helpers::errorMsg(4, "SQL", "user.sql will not open");
                return false;
            }
            std::string command = std::format(
                "insert into users (username, email, password), values ('{}','{}','{}');\n", 
                username, email, hashedPassword
            );

            userSqlFile << command;
            userSqlFile.close();
            return true;
        }
        catch (const std::runtime_error& ex) {
            Helpers::errorMsg(5, "creating new User", ex.what());
            return false;
        }
    }

    /* 
        Access keys are unique keys generals, rosa, or facility have, each unique.
        Basically API keys. If exposed publicly, remove/update it.
    */
    std::string createPrompt(std::string const& accessKey){ 

        if (accessKey.empty() || accessKey.length() != 700){return "invalid key";}
        // TODO: Access key logic here before prompt creation.
        if (!validKey(accessKey)){
            return "invalid key";
        }
        std::string prompt; getline(std::cin, prompt);
        return prompt;
    }

    bool validKey(std::string const accessKey){
        // 1: Check if it exists
        // 2. check it's not expired
        // 3. check if the holder exists
        // 4. if a worker, check if its work hours - they can only use it during their work hours
        //  (not needed for now)

        return false;
    }

    std::optional<std::unique_ptr<LinxAgent>> InstantiationProtocol(
        std::string_view const& id_,

    ){

        // TODO: NOT IMPLIMENTED 
        return nullptr;

            /*
                Brains act as physical components for GLINX's.
                Maybe one day get the software into some robots 👀
            */
            std::unique_ptr<Brain> brain = std::make_unique(Brain::Brain(string(id_), name, weight, requestId));
            if (!brain || brain == nullptr || brain.getId().empty()){ 
                Helpers::errorMsg(5, "Brain", "The brain wasn't created when making LINX");
                return nullptr;
            }

            std::string brainId = brain.getId().copy();
            std::unique_ptr<LinxAgent> agent = std::make_unique(LinxAgent(
                brain_id,
                ... // add rest 
            ))
            return agent;
        
        }
};
