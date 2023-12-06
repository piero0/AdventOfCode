#include <cstdint>
#include <iostream>
#include <fstream>
#include <limits>
#include <optional>
#include <string_view>
#include <unordered_map>
#include <sstream>
#include <vector>
#include <algorithm>
#include <format>

using namespace std::string_literals;
using u64 = std::uint64_t;
using Map = std::unordered_map<u64, u64>;
using Vec = std::vector<u64>;

struct Range {
    std::uint64_t dest{0}, src{0}, len{0};

    std::optional<u64> inRange(u64 v) {
        if (v>=src && v<(src+len)) {
            std::cout << std::format("match in {} {} {}\n", dest, src, len);
            return (v-src) + dest;
        }
        return std::nullopt;
    }
};

struct Mapping {
    std::vector<Range> ranges;

    void sortBySrc() {
        std::sort(ranges.begin(), ranges.end(), [](const auto& a, const auto& b) {
            return a.src < b.src;
        });
    }

    void sortByDest() {
        std::sort(ranges.begin(), ranges.end(), [](const auto& a, const auto& b) {
            return a.dest < b.dest;
        });
    }

    // just out of curiosity
    void checkGaps() {
        u64 last{0};

        for (auto& el : ranges) {
            if (last+1 != el.src && el.src !=  0) {
                std::cout << std::format("gap {}-{}\n", last, el.src);
            }
            last = el.src + el.len - 1;
        }
    }

    u64 map(u64 val) {
        for (auto& el : ranges) {
            if(auto res = el.inRange(val)) {
                std::cout << std::format("ret {}\n", res.value());
                return res.value();
            }
        }
        std::cout << "no map 1:1\n";
        return val;
    }

    void show() {
        for (auto& el : ranges) {
            std::cout << std::format("{} {} {}\n", el.dest, el.src, el.len);
        }
    }
};

Vec text2vec(std::string_view line) {
    Vec out;
    std::string d{};
    std::string l{line};
    std::istringstream iss{l};
    while(iss >> d) {
        out.emplace_back(std::stol(d));
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
        // std::cout << "#" << idx << " " << r.dest << " " << r.src << " " << r.len << " " << maps[idx].ranges.size() << "\n";
    }

    for(auto& el: maps) {
        std::cout << "\n";
        el.sortBySrc();
    }

    maps[maps.size()-1].sortByDest();

    u64 minLoc{std::numeric_limits<u64>::max()};

    for(auto& seed: seeds) {
        u64 last{seed};
        std::cout << std::format("\nseed {}\n", last);
        for(auto& el: maps) {
            last = el.map(last);
            std::cout << std::format("mapped {}\n", last);
        }
        minLoc = std::min(minLoc, last);
    }

    std::cout << std::format("\nminLoc {}\n", minLoc);

    return 0;
}

/*
1/ fill gaps (0-min, in the middle, max to int max)
2/ map input range to output ranges (how?)
3/ handle partial match (also how? :)
4/ repeat and solved :)
*/
