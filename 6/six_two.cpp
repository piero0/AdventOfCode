#include <cmath>
#include <fmt/core.h>
#include <fmt/ranges.h>
#include <iterator>
#include <sstream>
#include <string>
#include <fstream>
#include <vector>

using namespace std::string_literals;

using IntVec = std::vector<std::int64_t>;

IntVec sumSplit(const std::string& line) {
    std::string i{}, n{};
    std::istringstream iss{line};
    IntVec out{};
    while(std::getline(iss, i, ' ')) {
        if (i.find(':') != i.npos || i.empty()) continue;
        n += i;
    }
    out.emplace_back(std::stol(n));
    return out;
}

std::int64_t solution(std::int64_t t, std::int64_t d) {
    /* and now the real thinking beggins
    (t-n)*n
    tn - n^2 > d
    -n2 + tn > d
    -n2 + tn - d > 0

    1.6 > x > 5.3 => 2 3 4 5
    3.4 > x > 11.5 => 4 5 6 7 8 9 10 11
    10 > x > 20 => 11 12 13 14 15 16 17 18 19
    */
    auto dt = std::sqrt(t*t - 4*d);
    auto x1 = (-t - dt)/-2.;
    auto x2 = (-t + dt)/-2.;
    auto rx1 = std::floor(x1);
    auto rx2 = std::ceil(x2);

    auto newx2 = std::ceil(x2);
    if(newx2 == std::trunc(x2)) {
        newx2 += 1.;
        rx2 = newx2;
    }

    auto newx1 = std::ceil(x1);
    if(newx1 == std::trunc(x1)) {
        newx1 = std::floor(x1) - 1.;
        rx1 = newx1;
    }

    auto res = rx1 - rx2 + 1;

    fmt::print("x1: {} x2: {} res: {}\n", x1, x2, res);
    fmt::print("rx1: {} rx2: {}\n", rx1, rx2);

    return static_cast<std::int64_t>(res);
}

int main() {
    auto filename{"input.txt"s};
    std::ifstream file{filename};

    std::string time{}, distance{};

    std::getline(file, time);
    auto times = sumSplit(time);
    std::getline(file, distance);
    auto dist = sumSplit(distance);

    fmt::print("t {}\n", times);
    fmt::print("d {}\n", dist);

    std::int64_t sum{1};

    // in 23 we'll get zip like in python
    // so we need to wait few more years :)
    // but this for loop is also pretty and concise
    for (auto t = std::begin(times), d = std::begin(dist);
         t != std::end(times) && d != std::end(dist); t++, d++) {
            sum *= solution(*t, *d);
    }

    fmt::print("sum {}\n", sum);

    return 0;
}
// 36749313 >high
