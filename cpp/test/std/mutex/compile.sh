g++ -std=c++11 -pthread -fgnu-tm  -O2 -Wall -Wextra -pedantic -pthread -pedantic-errors test_mutex.cpp -lm  -latomic -lstdc++fs  && ./a.out

g++ -std=c++11 -pthread -fgnu-tm  -O2 -Wall -Wextra -pedantic -pthread -pedantic-errors test_shared_ptr.cpp -lm  -latomic -lstdc++fs  && ./a.out
