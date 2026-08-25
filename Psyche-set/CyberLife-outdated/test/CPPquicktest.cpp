#include <vector>
#include <map>
#include <sstream>

#include <fstream>
#include <string>
#include <iostream>
#include <chrono>
#include <optional>


class Memory{
private:
    std::chrono::system_clock::time_point date;
    std::vector<std::optional<std::string>> recent_memory;

    float watts;
    float brain_size;
public:
    Memory(const float& watts_, const float& power_) : 
    date(std::chrono::system_clock::now()){
        if (watts_ < 1.0f){
            throw std::invalid_argument("");
        } else if (watts_ > 20.0f){
            throw std::invalid_argument("");
        }
        this->watts = watts_;     
    }
    void ascends(float by=1){
        if (this->brain_size == 20.0){
            std::ostringstream oss;
            oss << "Brian have reached max limit: %f", this->brain_size;
            throw std::invalid_argument(oss.str());
        }
        this->watts = this->watts + by;f"
    }

};