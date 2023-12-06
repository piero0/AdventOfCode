#include <cstdint>
#include <iostream>
#include <fstream>
#include <string_view>
#include <unordered_map>
#include <sstream>
#include <vector>

using namespace std::string_literals;
using Map = std::unordered_map<std::uint64_t, std::uint64_t>;
using Vec = std::vector<std::uint64_t>;

struct Range {
    std::uint64_t dest{0}, src{0}, len{0};
};

struct Mapping {
    std::vector<Range> ranges;
};

Vec text2vec(std::string_view line) {
    Vec out;
    std::string d{};
    std::string l{line};
    std::istringstream iss{l};
    while(iss >> d) {
        out.emplace_back(std::stoi(d));
    }
    return out;
}

Vec parseSeeds(std::string_view line) {
    return text2vec(line.substr(line.find(':')+2));
}

Map parseSoils(std::string_view line) {
    return {};
}

int main() {
    auto filename{"input.txt"s};
    std::ifstream file{filename};
    Vec seeds;
    Map soils;
    std::vector<Mapping> maps;

    std::string line;
    std::getline(file, line);
    seeds = parseSeeds(line);
    for (auto el : seeds) {
        std::cout << el << " ";
    }
    std::cout << "\n";

    auto idx{-1};
    for(std::string line; std::getline(file, line);) {
        if (line.empty()) continue;
        if (line.ends_with(':')) {
            maps.push_back({});
            idx++;
            continue;
        }
        auto v = text2vec(line);
        Range r = {v[0], v[1], v[2]};
        maps[idx].ranges.emplace_back(r);
        std::cout << "#" << idx << " " << r.dest << " " << r.src << " " << r.len << " " << maps[idx].ranges.size() << "\n";
    }
    return 0;
}
