/* Why use c++ for a puzzle?
I don't know, probably it's one of these 'qualities'
a programmer has which makes him find some strange joy
in misery ;)
*/
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <string_view>
#include <vector>
#include <algorithm>

// namespace my {
// template<typename...  T>
// void print(const std::string_view format, T... args) {
//     std::cout << std::format(format, args...);
// }
// }
using Nums = std::vector<std::uint32_t>; 

struct Data {
    Nums winning, yours;
};

std::pair<std::string_view, std::string_view> splitLine(std::string_view line) {
    auto semi = line.find(':');
    auto bar = line.find('|');
    return {line.substr(semi+2, bar-semi-2), line.substr(bar+2)};
}

Nums toVector(std::string_view numbers) {
    Nums n;
    for(std::size_t s = 0, p = numbers.find(' ');s != numbers.npos;p = numbers.find(' ', s)) {
        if (p == s) {
            s++;
            continue;
        }
        if (p == numbers.npos) {
            break;
        }
        std::string num{numbers.substr(s, p-s)}; //yes I know :)
        n.emplace_back(std::stoi(num));
        s = p+1;
    }
    return n;
}

Data getData(std::string_view line) {
    auto [winning, yours] = splitLine(line);
    // std::cout << winning << " x " << yours << "\n";
    return Data{toVector(winning), toVector(yours)};
}

std::uint32_t compare(const Nums& a, const Nums& b) {
    auto m{0};
    auto i{0};
    //TODO find the bug
    for (auto& el : a) {
        if (el == b[i]) {
            m++;
            i++;
        } else if (el < b[i]) {
            continue;
        } else {
            while(b[i] < el) {++i;};
        }
    }
    return m;
}

int main() {
    std::ifstream file{"input.txt"};

    std::uint64_t sum{0};
    for(std::string line; std::getline(file, line);) {
        // std::cout << line << "\n";
        auto data = getData(line);
        std::sort(std::begin(data.winning), std::end(data.winning));
        std::sort(std::begin(data.yours), std::end(data.yours));
        auto m = compare(data.winning, data.yours);
        if (m > 0) {
            sum += (1<<m);
            std::cout << m << " " << (1<<m) << "\n";
        }
    }
    std::cout << sum << "\n";
}
// 384 too low