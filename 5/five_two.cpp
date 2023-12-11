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
#include <fmt/core.h>
#include <fmt/ranges.h>

using namespace std::string_literals;
using u64 = std::uint64_t;
using Map = std::unordered_map<u64, u64>;
using Vec = std::vector<u64>;

struct Range {
    std::uint64_t dest{0}, src{0}, len{0};

    std::optional<u64> inRange(u64 v) {
        if (v>=src && v<(src+len)) {
            fmt::print("match in: {}\n", print());
            return (v-src) + dest;
        }
        return std::nullopt;
    }

    std::string print() const {
        return fmt::format("dst: {} src: {} len: {}", dest, src, len);
    }
};

struct Mapping {
    std::vector<Range> ranges;
    const std::string name{};

    Mapping(): name("noname") {}
    Mapping(const std::string& name): name(name) {}

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
    std::vector<Range> checkGaps() {
        u64 last{0};

        std::vector<Range> missing;

        for (auto& el : ranges) {
            if (last+1 != el.src && el.src !=  0) {
                fmt::print("gap {}-{}\n", last, el.src);
                missing.emplace_back(Range{last, last, el.src-last});
            }
            last = el.src + el.len - 1;
        }

        return missing;
    }

    void fixLast() {
        auto lastR = ranges[ranges.size()-1];
        auto end = lastR.dest + lastR.len;
        if (end < std::numeric_limits<std::uint64_t>::max()) {
            auto max = std::numeric_limits<std::uint64_t>::max();
            auto r = Range{end, end, 1000000000};
            fmt::print("adding end {}\n", r.print());
            ranges.emplace_back(r);
        }
    }

    u64 map(u64 val) {
        for (auto& el : ranges) {
            if(auto res = el.inRange(val)) {
                fmt::print("ret {}\n", res.value());
                return res.value();
            }
        }
        fmt::print("no map 1:1\n");
        return val;
    }

    Mapping map(Range i) const {
        // załóżmy że mamy wszystkie range bez gapów
        // potem się zobaczy czy trzeba uzupełnić czy da się bez

        /* input dest len
            dest src len
        */
        fmt::print("input: {}\n", i.print());
        Mapping out{name};

        //auto last = ranges[ranges.size()-1];
        //if (i.dest >= last.dest+last.len) {
        //    fmt::print("early out {}\n", i.dest);
        //    out.ranges.emplace_back(Range({i.dest, i.dest, i.len}));
        //    return out;
        //}

        for (auto& d : ranges) {
            fmt::print("dest: {}\n", d.print());
            /* d(estination)
                src................src+len
                       i.dest............i.dest+len  op1
                     i.dest...len  op2
                1................10  1,10
                      3...............15 3,13
                      3...5 3,3
                
            */
            auto dEnd{d.src+d.len-1};
            auto iEnd{i.dest+i.len-1};

            if (i.dest >= d.src && i.dest <= dEnd) {
                std::int64_t dt = std::abs(static_cast<std::int64_t>(i.dest - d.src));
                auto newDest = (i.dest-d.src) + d.dest;
                u64 newLen{0};

                auto endDt = static_cast<std::int64_t>(iEnd - dEnd);

                // input end inside dest => endDt < 0
                if(endDt > 0) {
                    newLen = dEnd - i.dest;
                    i.len = endDt;
                    i.dest = dEnd + 1;
                } else {
                    newLen = i.len;
                    i.len = 0;
                }
                auto m = Range{newDest, 0, newLen};
                fmt::print("match: {}\n", m.print());
                out.ranges.emplace_back(m);
            }
            if(i.len == 0) {
                fmt::print("range mapped fully\n");
                break;
            }
        }
        if (i.len != 0) {
            fmt::print("!leftover\n");
        }
        return out;
    }

    void show() {
        for (auto& el : ranges) {
            fmt::print("{}\n", el.print());
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
                fmt::print("{}\n", el.print());
            }
        }
        fmt::print("\n");
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

std::uint64_t findLocation(const Mapping& in, const std::vector<Mapping>& maps, int i) {
    fmt::print("i: {} len: {} name: {}\n", i, in.ranges.size(), maps[i].name);
    std::uint64_t min{std::numeric_limits<u64>::max()};

    if (i >= maps.size() ) {
        fmt::print("Results: \n");
        for(auto& el: in.ranges) {
            fmt::print("{}\n", el.print());
            min = std::min(min, el.dest);
        }
        fmt::print("\n new min: {}\n", min);
        return min;
    }
    for (auto& r : in.ranges) {
        fmt::print("> {}\n", r.print());
        auto newMap = maps[i].map(r);
        min = std::min(min, findLocation(newMap, maps, i+1));
    }
    fmt::print("{} end\n", i);
    return min;
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
    fmt::print("seeds: {}\n", seeds);

    auto idx{-1};
    for(std::string line; std::getline(file, line);) {
        if (line.empty()) continue;
        if (line.ends_with(':')) {
            maps.push_back({line});
            idx++;
            continue;
        }
        auto v = text2vec(line);
        Range r = {v[0], v[1], v[2]};
        maps[idx].ranges.emplace_back(r);
        // std::cout << "#" << idx << " " << r.dest << " " << r.src << " " << r.len << " " << maps[idx].ranges.size() << "\n";
    }

    for(auto& el: maps) {
        el.sortBySrc();
        auto mis = el.checkGaps();
        for (auto& e: mis) {
            fmt::print("filling gap: {}\n", e.print());
            el.ranges.push_back(e);
        }
        if (mis.size() > 0) {
            el.sortBySrc();
        }
        el.fixLast();
    }

    // maps[maps.size()-1].sortByDest();

    u64 minLoc{std::numeric_limits<u64>::max()};

    Mapping input;
    for (int i=0; i<seeds.size(); i+=2) {
        input.ranges.emplace_back(Range{seeds[i], 0, seeds[i+1]});
    }

    minLoc = findLocation(input, maps, 0);

    fmt::print("\nminLoc {}\n", minLoc);

    // testMapping();
    return 0;
}

/*
1/ fill gaps (0-min, in the middle, max to int max)
2/ map input range to output ranges (how?)
3/ handle partial match (also how? :)
4/ repeat and solved :)
*/
