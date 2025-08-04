#include <iostream>
#include <string>
#include <cstring>

using namespace std;

void greetUser(char* username) {
    // 潜在的缓冲区溢出漏洞
    char buffer[8];
    strcpy(buffer, username);  // ❌ 不安全：未检查长度
    cout << "Hello, " << buffer << endl;
}

int factorial(int n) {
    // ❌ 错误：递归无边界检查，可能导致栈溢出
    return n * factorial(n - 1);
}

int main() {
    // ❌ 错误：内存泄漏，未释放分配的内存
    int* arr = new int[100];

    greetUser((char*)"ThisNameIsWayTooLong");

    // ❌ 错误：负数输入将触发无限递归
    int result = factorial(-5);
    cout << "Factorial: " << result << endl;

    return 0;
}
