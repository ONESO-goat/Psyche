
#include "helpers/helpers.h"
#include "schema/metadata_structs.h"
#include <cassert>
#include <string_view>
// g++ -std=c++20 main.cpp helpers/helpers.cpp -o program -luuid
using namespace std;

Name nameTest = {"john", "", "doe"};
string idTest = "1";

// g++ -std=c++20 main.cpp helpers/helpers.cpp -o program -luuid  # WORKS

void uuidTest(){
    cout << "1: ID TEST \n";
    std::string_view id = Helpers::generateId(Group::LINX, "music");
    cout << " Generated ID == " << id << endl;
    assert(id.length() > 0);
    assert(!id.empty());

    cout << "2: ACCESSKEY TEST \n";
    std::string_view accessKey = Helpers::generateAccessKeyLinux("rosa");
    cout << "Access key == " << accessKey << " of length == " << accessKey.length() << endl;

    assert(accessKey.length() > 0);
    assert(!accessKey.empty());
}
auto createLinxTest(){

}

int main(){
    uuidTest();
    return 0;
}
