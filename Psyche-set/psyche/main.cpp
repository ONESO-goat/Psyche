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

void uuidTest(){
    cout << "1: ID TEST \n";
    std::string id = Helpers::generateId(Group::LINX, "music");
    cout << " Generated ID == " << id << endl;
    assert(id.length() > 0);
    assert(!id.empty());

    cout << "2: ACCESSKEY TEST \n";
    std::string accessKey = Helpers::generateAccessKeyLinux("rosa");
    cout << "Access key == " << accessKey << " of length == " << accessKey.length() << endl;

    assert(accessKey.length() > 0);
    assert(!accessKey.empty());
}
auto createBrainTest(){
    auto brain = std::make_unique<Brain>(
        "id0", nameTest, 5, Group::LINX, "Julius-123"
    );
    for (const auto [key, values] : brain->getBrainData()){
        cout << "Current key == " << key << endl;
    }

}

auto createLinxTest(std::string key){
    Database database = Database(key);
    auto l = database.createLinx(
        "julius-1",
        "julius",
        "testing",
        nameTest
    );
    assert(l == true);
    return l;
}

auto dateTest(bool UTC=false){
    return Helpers::getDate(UTC);
}

struct test{
    Name name = name;
};

int main(){
    createLinxTest("bad key");
    return 0;
}
