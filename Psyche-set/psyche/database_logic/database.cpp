/*
database.cpp

Database logic, where we edit sql files, add, remove, etc...
*/


#include "database.h"



    Database::Database(std::string const& passkey) : passkey(passkey) {
        if (passkey != "admin123"){std::cerr << "access denied" << std::endl; return;}
    }

    bool Database::linxConnection(
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
   
    bool Database::createLinx(
        std::string const& requestId,
        std::string const& ownerType, 
        std::string reason, 
        Name const& name,
        std::string const& nicheId,
        float weight,
        bool _createBrain
    ) {      
        try {
         
            std::fstream sqlFile("sql_models/GLINX.sql", std::ios::app);
            if (!sqlFile.is_open()){
                Helpers::errorMsg(5, "SQL", "GLINX.sql file will not open during linx creation.");
                return false;
            }

            
            Group type = std::set<std::string>{"rosa", "lina", "general"}.contains(ownerType) ? Group::MANAGER : Group::LINX;
            
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

            std::string command = std::format(
                "insert into Linx\n"
                " (name, {0}_id, niche_id, linx_type)\n"
                " values ('{1}', '{2}', '{3}', '{4}')\n",
                ownerType, fullName, requestId, nicheId, type 
            );
            sqlFile << command;
            sqlFile.close();
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

