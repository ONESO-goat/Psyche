/*
database.cpp

Database logic, where we edit sql files, add, remove, etc...
*/


#include <format>
#include <helpers/imports.h>
#include <chrono>
#include <fstream>
#include <set>
#include <string>
#include <vector>
#include <unordered_map>

import Helpers;

using namespace std;
class Database {
private:
    string passkey;

public:
    Database(string const passkey) : passkey(passkey) {}

    bool linxConnection(
        string const& linxId, 
        string const& ownerType,
        string const& ownerId
    ) {
        // TODO: not implemented
        string command = format("select linx where linx_id = {}?", linxId);
        unordered_map<string, string> commands = {
            {"rosa", ""},
            {"user", ""},
            {"general", ""}
        };
        return true;
    }
   
    bool createLinx(
        string const& requestId,
        string const& ownerType, 
        string reason = "personal", 
        Name const& name = Name("Linx", "", "Psy"),
       string nicheId = "",
        float weight = 5.0
    ) {      
        try {
         
            fstream sqlFile("sql_models/GLINX.sql", ios::app);
            if (!sqlFile.is_open()){
                Helpers::errorMsg(5, "SQL", "GLINX.sql file will not open during linx creation.");
                return false;
            }
            string type = set<string>{"rosa", "lina", "general"}.contains(ownerType) ? "manager" : "personal";
            
            string id_ = Helpers::generateId("linx", ownerType);
            if (id_.empty()){
                cerr << Helpers::errorMsg(2, "generating ID", format("Id returned NULL. Id == {}", id_)) << endl;
                return false;
            } 
            
            string fullName = name.middle != "" ? 
            format("{}{}{}", name.first, name.middle, name.last) :
            format("{} {}", name.first, name.last);

            string command = format(
                "insert into Linx\n"
                " (name, {0}_id, niche_id, linx_type)\n"
                " values ('{1}', '{2}', '{3}', '{4}')\n",
                ownerType, fullName, requestId, nicheId, type 
            );
            sqlFile << command;
            sqlFile.close();

            
            // vector<string> commands = {
            //     format("create linx where name = {}", fullName),
            //     format("{}_id = {}", ownerType, requestId),
            //     format("niche_id = {}", nicheId),
            //     format("linx_type = {}", type)
            // };
            
            // // FIX: Removed Python-style named arguments. Must be positional.
            // Brain brain(id_, name, weight, requestId);
            return true;

        } catch (const runtime_error& ex){
            Helpers::errorMsg(5, "Creating LINX", ex.what());
            return false;
        }
    }

    bool addUser(
        string const& username,
        string const& email,
        string const& hashedPassword
    ) {
        try {
            fstream userSqlFile("sql_models/user.sql", ios::app);
            if (!userSqlFile.is_open()) {
                cerr << Helpers::errorMsg(4, "SQL", "user.sql will not open");
                return false;
            }
            string command = format(
                "insert into users (username, email, password), values ('{}','{}','{}');\n", 
                username, email, hashedPassword
            );

            userSqlFile << command;
            userSqlFile.close();
            return true;
        }
        catch (const runtime_error& ex) {
            Helpers::errorMsg(5, "creating new User", ex.what());
            return false;
        }
    }

    /* Access keys are unique keys generals, rosa, or facility have, each unique.
        Basically API keys. If exposed publicly, remove/update it.
    */
    string createPrompt(string const& accessKey){ 

        if (accessKey.empty() || accessKey.length() != 700){return "invalid key";}
        // TODO: Access key logic here before prompt creation.
        if (!validKey(accessKey)){
            return "invalid key";
        }
        string prompt; getline(cin, prompt);
        return prompt;
    }

    bool validKey(string const accessKey){
        // 1: Check if it exists
        // 2. check it's not expired
        // 3. check if the holder exists
        // 4. if a worker, check if its work hours - they can only use it during their work hours
        //  (not needed for now)

        return false;
    }
};
