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

    int* ptr = new int[10];
    // ❌ 错误：未释放内存
    // delete[] ptr;  // 如果取消注释，将修复内存泄漏

    int zero = 0;
    // ❌ 错误：除以零将导致未定义行为
    int division = 10 / zero;  // ❌ 不安全：除以零
    cout << "Division result: " << division << endl;

    // ❌ 错误：使用未初始化的变量
    int uninitializedVar;
    cout << "Uninitialized variable" << uninitializedVar << endl;  // ❌ 不安全：未初始化变量
    
    // ❌ 错误：使用空指针
    int* nullPtr = nullptr;
    cout << "Dereferencing null pointer: " << *nullPtr << endl;  // ❌ 不安全：空指针解引用

    // ❌ 错误：使用未定义的行为
    int* undefinedPtr;
    cout << "Undefined pointer value: " << *undefinedPtr << endl;  // ❌ 不安全：未定义行为
    
    // ❌ 错误：数组越界访问
    int arr2[5] = {1, 2, 3, 4, 5};
    cout << "Out of bounds access: " << arr2[10] << endl;  // ❌ 不安全：数组越界

    // ❌ 错误：使用已释放的内存
    int* danglingPtr = new int(42);
    delete danglingPtr;
    cout << "Dangling pointer value: " << *danglingPtr << endl;  // ❌ 不安全：悬空指针
    
    // ❌ 错误：使用未定义的行为
    int* uninitializedPointer;
    cout << "Uninitialized pointer value: " << *uninitializedPointer << endl;  // ❌ 不安全：未初始化指针

    // ❌ 错误：使用未定义的行为
    int* invalidPointer = (int*)0x12345678;
    cout << "Invalid pointer value: " << *invalidPointer << endl;  // ❌ 不安全：无效指针
    
    // ❌ 错误：使用未定义的行为
    int* outOfBoundsPointer = arr2 + 10;
    cout << "Out of bounds pointer value: " << *outOfBoundsPointer << endl;  // ❌ 不安全：越界指针
    return 0;
}
