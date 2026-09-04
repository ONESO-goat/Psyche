// main.cpp

#include <cassert>
#include <memory>
#include <string_view>
#include "brainAnomaly/brain.h"
#include "helpers/helpers.h"
#include "schema/metadata_structs.h"
#include "database_logic/database.h"

using namespace std;


Name nameTest = {"john", "", "doe"};
string idTest = "1";
int c = 1;
vector<std::string> errors;
Database database = Database("admin123");

auto uuidTest(){
   
    std::string id = Helpers::generateId(Group::LINX, "music");

    // assert(id.length() > 0);
    // assert(!id.empty());

    std::string accessKey = Helpers::generateAccessKeyLinux("rosa");

    // assert(accessKey.length() > 0);
    // assert(!accessKey.empty());
    return accessKey;
}
bool createBrainTest(){
    auto brain = std::make_unique<Brain>(
        "id0", nameTest, 5, Group::LINX, "Julius-123"
    );

    return brain->getId() != "";

}


bool createDatabase(std::string const& passkey){
    //Database database = Database(passkey);
    return database.does_not_exist();
}

bool createLinxTest(std::string key, string requestId){
    auto l = database.createLinx(
        requestId,              // The Id of the person/object requesting
        "user",      // User, general
        "testing",      // The reason for creating
        nameTest          // Name for the created LINX
    );
    // assert(l == true);
    return l;
}

bool createUser(){
    std::string username = "test_user";
    std::string testPassword = "theBestPasswordEver";
    std::string email = "test@company.com";

    auto l = database.addUser(username, email, testPassword);
    return l;
}

auto dateTest(bool UTC=false){
    return Helpers::getDate(UTC);
}

void appendErrors(bool e, std::string const& errorDetails){
    if (!e){
        errors.push_back(
            to_string(c) + ": " + errorDetails
        );
        c++;
    }
}

void tests(std::string passkey){
    bool e;
    e = createDatabase(passkey);
    if (e){
        errors.push_back(
            to_string(c) + ": Database was not created"
        );
        c++;
    }

    e = createUser();
    appendErrors(e, "User was not created");

    e = createBrainTest();
    appendErrors(e, "Brain or Brain ID were not created");
 
    if (e){
        std::string id; cin >> id;
        
        e = createLinxTest(passkey, id);
        appendErrors(e, "Linx was not created");
    }
    // e = createLinxTest(passkey, "USER-ad294e06-1638-4392-813d-554f657bf5ce-u");
    // appendErrors(e, "Linx was not created");

    
    // e = typeof(dateTest()) == std::chrono::year_month_day ;
    // appendErrors(e, "Datetime was not created");

    cout << "There are " << errors.size() << " errors." << endl;
    for (const std::string& error : errors){
        std::cerr << error << std::endl;
    }
}


int main(){
    std::string passkey = "admin123";
    tests(passkey);
    return 0;
}
