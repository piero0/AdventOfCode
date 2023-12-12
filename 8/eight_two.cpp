#include <array>
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <fmt/core.h>
#include <fmt/ranges.h>
#include <iterator>
#include <string>
#include <unordered_set>
#include <vector>

using namespace std::string_literals;

using str3 = std::array<std::string, 3>;
using int2 = std::array<std::uint16_t, 2>;
using strVec = std::vector<str3>;

int main() {
    std::unordered_set<std::string> names;
    std::string strMoves{};
    strVec strNodes;
    std::ifstream file{"input.txt"s};

    std::getline(file, strMoves);

    fmt::print("_{}_ {}\n", strMoves, strMoves.size());

    std::string line{};
    while(std::getline(file, line)) {
        if (line.empty()) continue;
        auto name = line.substr(0, 3);
        auto left = line.substr(7, 3);
        auto right = line.substr(12, 3);
        names.insert(name);
        names.insert(right);
        names.insert(left);
        strNodes.emplace_back(str3{name, left, right});
    }

    //prepare to convert names to indecies
    std::vector<std::string> sortedNames(names.begin(), names.end());
    std::sort(sortedNames.begin(), sortedNames.end());

    std::vector<std::array<std::uint16_t, 2>> nodes(sortedNames.size());

    //convert strNodes to intNodes
    auto start = sortedNames.begin();
    auto startIndex{-1};
    for (const auto& el : strNodes) {
        auto i1 = std::lower_bound(sortedNames.begin(), sortedNames.end(), el[0]);
        auto i2 = std::lower_bound(sortedNames.begin(), sortedNames.end(), el[1]);
        auto i3 = std::lower_bound(sortedNames.begin(), sortedNames.end(), el[2]);
        auto d1 = std::distance(start, i1);
        auto d2 = std::distance(start, i2);
        auto d3 = std::distance(start, i3);
        nodes[d1] = int2{static_cast<std::uint16_t>(d2), static_cast<std::uint16_t>(d3)};
        if (startIndex < 0) {
            startIndex = d1;
        }
    }

    //moves to idx
    std::vector<std::size_t> moves;
    for(const auto& el: strMoves) {
        moves.emplace_back((el == 'L') ? 0 : 1);
    }

    //find starts and ends
    std::vector<std::size_t> startIdx;
    std::unordered_set<std::size_t> ends;

    auto it0 = sortedNames.begin();

    for (auto it = sortedNames.begin(); it != sortedNames.end(); it++) {
        auto lastChar = (*it)[2];
        if (lastChar == 'A') {
            fmt::print("A {}\n", *it);
            startIdx.emplace_back(std::distance(it0, it));
        } else if(lastChar == 'Z') {
            fmt::print("Z {}\n", *it);
            ends.insert(std::distance(it0, it));
        }
    }

    //simul
    auto steps{0L};
    auto d = moves.begin();
    std::vector<std::size_t> results;

    for(auto it = startIdx.begin(); it != startIdx.end(); it++) {
        while(true) {
            *it = nodes[*it][*d];
            d++;
            steps++;
            if (ends.contains(*it)) {
                d = moves.begin();
                results.emplace_back(steps);
                steps = 0;
                break;
            }
            if (d == moves.end()) {
                d = moves.begin();
            }
        }
    }

    fmt::print("\nsteps {}\n", results);
    //todo: of course c++ does not have a lcm
    //for 2+ elements so you need to chain it yourself
    return 0;
}
