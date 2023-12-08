#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <limits>
#include <optional>
#include <string_view>
#include <unordered_map>
#include <sstream>
#include <vector>
#include <algorithm>
// #include <format>
#include <fmt/core.h>

using namespace std::string_literals;
using u64 = std::uint64_t;
using Map = std::unordered_map<u64, u64>;
using Vec = std::vector<u64>;

struct Range {
    std::uint64_t dest{0}, src{0}, len{0};

    std::optional<u64> inRange(u64 v) {
        if (v>=src && v<(src+len)) {
            std::cout << fmt::format("match in {} {} {}\n", dest, src, len);
            return (v-src) + dest;
        }
        return std::nullopt;
    }

    void print() {
        fmt::print("dst: {} src: {} len: {}\n", dest, src, len);
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
                std::cout << fmt::format("gap {}-{}\n", last, el.src);
            }
            last = el.src + el.len - 1;
        }
    }

    u64 map(u64 val) {
        for (auto& el : ranges) {
            if(auto res = el.inRange(val)) {
                std::cout << fmt::format("ret {}\n", res.value());
                return res.value();
            }
        }
        std::cout << "no map 1:1\n";
        return val;
    }

    Mapping map(Range i) {
        // załóżmy że mamy wszystkie range bez gapów
        // potem się zobaczy czy trzeba uzupełnić czy da się bez
        Mapping out;
        for (auto& d : ranges) {
            d.print();
            /* d(estination)
                src................src+len
                       i.dest............i.dest+len  op1
                     i.dest...len  op2
                1................10  1,10
                      3...............15 3,13
                      3...5 3,3
                
            */
            auto dEnd{d.src+d.len};
            auto iEnd{i.src+i.len};

            if (i.dest >= d.src && i.dest < dEnd) {
                std::int64_t dt = std::abs(static_cast<std::int64_t>(i.dest - d.src));
                auto newSrc = d.src + dt;
                u64 newLen{0};

                auto endDt = iEnd - dEnd;

                if(endDt > 0) {
                    newLen = dEnd - i.dest;
                    i.len = endDt;
                    i.dest = dEnd + 1;
                } else {
                    newLen = i.len;
                    i.len = 0;
                }

                out.ranges.emplace_back(Range{0, newSrc, newLen});
            }
            if(i.len == 0) {
                break;
            }
        }
        return out;
    }

    void show() {
        for (auto& el : ranges) {
            std::cout << fmt::format("{} {} {}\n", el.dest, el.src, el.len);
        }
    }
};

void testMapping() {
    std::vector<Range> rngs {{3, 0, 5}, {3, 0, 15}, {3, 0, 10}, {1, 0, 10}};
    
    Mapping m1;
    m1.ranges.emplace_back(Range{5, 1, 10});

    for(auto& r: rngs) {
        fmt::print("input range {} {} {}\n", r.dest, r.src, r.len);
        auto out = m1.map(r);
        fmt::print("output map {}\n", out.ranges.size());
        if (out.ranges.size() > 0) {
            for(auto& el: out.ranges) {
                el.print();
            }
        }
    }
}

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

    // maps[maps.size()-1].sortByDest();

    u64 minLoc{std::numeric_limits<u64>::max()};

    Range r{0, seeds[0], seeds[1]};

    fmt::print("range {} {} {}\n", r.dest, r.src, r.len);
    

    std::cout << fmt::format("\nminLoc {}\n", minLoc);

    testMapping();
    return 0;
}

/*
1/ fill gaps (0-min, in the middle, max to int max)
2/ map input range to output ranges (how?)
3/ handle partial match (also how? :)
4/ repeat and solved :)
*/
