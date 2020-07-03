#include <iostream>
#include <vector>

using namespace std;

struct Point
{
	int x;
	int y;
};

 void vscpp(int * args)
{
	int a;
	cout << "123";
	cin >> a;
	bool b = true;
	bool c = -b;
	if (c)
	{
		cout << "c is true"<<endl;
	}
	int d = 12 / 3 * 4 + 5 * 15 + 24 % 4 / 3;
	cout << d;
	Point pi;
	pi.x = 3;
	pi.y = 2;
	cout << pi.y << pi.x << endl;
	cin >> a;
}