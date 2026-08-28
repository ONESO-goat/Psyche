#include <format>
#include <imports.h>
#include <chrono>
#include <fstream>
#include <set>
import Helpers;

using namespace std;



class Database{
private:
    /*
        protective layer
    */
    string passkey;

public:

    Database(string const passkey){

    }

    bool linxConnection(
        string const& linxId, 
        string const& ownerType,
        string const& ownerId // Rosa, User, General, ETC...
    ){
        string command = format("select linx where linx_id = {0}?", linxId);
        unordered_map<string, string> commands = {
            {"rosa", ""},
            {"user", ""},
            {"general", ""}
        };


    }
   
    bool createLinx(
        Name const& name,
        string const& requestId,
        string reason = "personal", // Personal or depth reason from a general
        string const& ownerType, 
        string nicheId = "",
        float weight = 5.0
    ){      
    
         try   {     
            string type = set<string>{
                "rosa", 
                "lina", 
                "general"
            }.contains(ownerType) ? "manager" : "personal";
            
        
            string id_ = Helpers::generateId("linx", ownerType);
            if (id_.empty()){
                cerr << Helpers::errorMsg(2, "generating ID", format("Id returned NULL. Id == {}", id_)) << endl;
                return false;
            } 
            
            string fullName = format("{}{}{}", name.first, name.middle, name.last);
            vector<string> commands = {
                format("create linx where name = {}", fullName),
                format("{}_id = {}", ownerType, requestId),
                format("niche_id = {}", nicheId)
            
            };
            Brain brain = Brain::Brain(id_=id_, name=name, weight_=weight, creatorId=requestId);
            
            


        } catch (const runtime_error ex){
            Helpers::errorMsg(5, "Creating LINX", ex.what());
            return false;
        }


   
    }
    bool addUser(
        string const& username,
        string const& email,
        string const& hashedPassword
    ){
        try{

            fstream userSqlFile("sql_models/user.sql", ios::app);
            if (!userSqlFile.is_open()) {
                cerr << Helpers::errorMsg(4,  "SQL", "user.sql will not open");
                return false;
            }
            string command = format(
                "insert into users (username, email, password), ({0},{1},{2})", 
                username, email, hashedPassword
            );

            userSqlFile >> command;
            userSqlFile.close();
            return true;
        }
        catch (const runtime_error ex) {
            Helpers::errorMsg(5, "creating new User", ex.what());
            return false;
            
        }
    }
};