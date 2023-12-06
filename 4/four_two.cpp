/* Why use c++ for a puzzle?
I don't know, probably it's one of these 'qualities'
a programmer has which makes him find some strange joy
in misery ;)
*/
#include <cstdint>
#include <fstream>
#include <iostream>
#include <iterator>
#include <string>
#include <string_view>
#include <vector>
#include <algorithm>
#include <unordered_map>

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
            if (s < numbers.size()) {
                std::string num{numbers.substr(s)};
                n.emplace_back(std::stoi(num));
            }
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
    return Data{toVector(winning), toVector(yours)};
}

std::uint32_t compare(const Nums& a, const Nums& b) {
    Nums out;
    std::set_intersection(a.begin(), a.end(), b.begin(), b.end(), std::back_inserter(out));
    return out.size();
}

int main() {
    std::ifstream file{"input.txt"};

    using I2Imap = std::unordered_map<std::uint32_t, std::uint32_t>;
    I2Imap wins;
    I2Imap cards;

    for (auto i=1; i<=199; i++) {
        cards[i] = 1;
    }

    std::uint64_t sum{0};
    auto cardno{1};
    for(std::string line; std::getline(file, line);) {
        auto data = getData(line);
        std::sort(std::begin(data.winning), std::end(data.winning));
        std::sort(std::begin(data.yours), std::end(data.yours));
        auto m = compare(data.winning, data.yours);
        wins[cardno] = m;
        std::cout << "#" << cardno << " " << m << "\n";

        while(m > 0) {
            cards[cardno+(m--)] += cards[cardno];
        }

        for (auto i=1; i<=cardno+10; i++) {
            std::cout << i << "-" << cards[i] << " ";
            sum += cards[i];
        }
        std::cout << " sum: " << sum << "\n";
        sum = 0;

        cardno++;
    }
    for (auto el : cards) {
        sum += el.second;
    }
    std::cout << sum << "\n";
}
// 5539497 high
// 5539496
