// main.cpp
#include "helpers/helpers.h"
#include "schema/metadata_structs.h"
#include <cassert>
#include <memory>
#include <string_view>
#include "brainAnomaly/brain.h"

// g++ -std=c++20 main.cpp helpers/helpers.cpp -o program -luuid
using namespace std;

Name nameTest = {"john", "", "doe"};
string idTest = "1";

// g++ -std=c++20 main.cpp helpers/helpers.cpp -o program -luuid  # WORKS

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
    auto brain = std::make_unique<Brain>("id0", nameTest, 5, Group::LINX, "Julius-123");
    cout << " Brain ID == " << brain->getId() << endl;
}

auto dateTest(bool UTC=false){
    return Helpers::getDate(UTC);
}
int main(){
    auto d = Helpers::getDate(true);
    cout << d << endl;
    return 0;
}
