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

    // ❌ 错误：使用未定义的行为
    int* nullPointer = nullptr;
    cout << "Dereferencing null pointer: " << *nullPointer << endl;  // ❌ 不安全：空指针解引用

    // ❌ 错误：使用未定义的行为
    int* danglingPointer = new int(100);
    delete danglingPointer;
    cout << "Dangling pointer value: " << *danglingPointer << endl;  // ❌ 不安全：悬空指针

    // ❌ 错误：使用未定义的行为
    int* invalidMemoryAccess = (int*)0xFFFFFFFF;
    cout << "Invalid memory access: " << *invalidMemoryAccess << endl;  // ❌ 不安全：无效内存访问

    // ❌ 错误：使用未定义的行为
    int* uninitializedMemory = new int;
    cout << "Uninitialized memory value: " << *uninitializedMemory << endl;  // ❌ 不安全：未初始化内存

    // ❌ 错误：使用未定义的行为
    int* freedMemory = new int(200);
    delete freedMemory;
    cout << "Freed memory value: " << *freedMemory << endl;  // ❌ 不安全：已释放内存访问

    // ❌ 错误：使用未定义的行为
    int* invalidPointerAccess = (int*)0xDEADBEEF;
    cout << "Invalid pointer access: " << *invalidPointerAccess << endl;  // ❌ 不安全：无效指针访问                                                
    // ❌ 错误：使用未定义的行为
    int* invalidArrayAccess = arr2 + 20;
    cout << "Invalid array access: " << *invalidArrayAccess << endl;  // ❌ 不安全：无效数组访问

    // ❌ 错误：使用未定义的行为
    int* nullPointerDereference = nullptr;
    cout << "Null pointer dereference: " << *nullPointerDereference << endl;  // ❌ 不安全：空指针解引用

    // ❌ 错误：使用未定义的行为
    int* danglingPointerAccess = new int(300);
    delete danglingPointerAccess;
    cout << "Dangling pointer access: " << *danglingPointerAccess << endl;  // ❌ 不安全：悬空指针访问

    // ❌ 错误：使用未定义的行为
    int* invalidMemoryAccess2 = (int*)0xBADF00D;
    cout << "Invalid memory access 2: " << *invalidMemoryAccess2 << endl;  // ❌ 不安全：无效内存访问

    // ❌ 错误：使用未定义的行为
    int* uninitializedPointer2;
    cout << "Uninitialized pointer value 2: " << *uninitializedPointer2 << endl;  // ❌ 不安全：未初始化指针

    // ❌ 错误：使用未定义的行为
    int* outOfBoundsPointer2 = arr2 + 100;
    cout << "Out of bounds pointer value 2: " << *outOfBoundsPointer2 << endl;  // ❌ 不安全：越界指针

    // ❌ 错误：使用未定义的行为
    int* nullPointer2 = nullptr;
    cout << "Dereferencing null pointer 2: " << *nullPointer2 << endl;  // ❌ 不安全：空指针解引用

    // ❌ 错误：使用未定义的行为
    int* danglingPointer2 = new int(400);
    delete danglingPointer2;
    cout << "Dangling pointer value 2: " << *danglingPointer2 << endl;  // ❌ 不安全：悬空指针

    // ❌ 错误：使用未定义的行为
    int* invalidPointerAccess2 = (int*)0xCAFEBABE;
    cout << "Invalid pointer access 2: " << *invalidPointerAccess2 << endl;  // ❌ 不安全：无效指针访问
    
    // ❌ 错误：使用未定义的行为
    int* invalidArrayAccess2 = arr2 + 50;
    cout << "Invalid array access 2: " << *invalidArrayAccess2 << endl;  // ❌ 不安全：无效数组访问

    // ❌ 错误：使用未定义的行为
    int* nullPointerDereference2 = nullptr;
    cout << "Null pointer dereference 2: " << *nullPointerDereference2 << endl;  // ❌ 不安全：空指针解引用
    return 0;
}
