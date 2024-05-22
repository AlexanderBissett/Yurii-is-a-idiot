

__int64 start()
{
    HANDLE StdHandle; // rbx
    DWORD NumberOfCharsWritten; // [rsp+40h] [rbp+8h] BYREF

    StdHandle = GetStdHandle(0xFFFFFFF5);
    WriteConsoleW(StdHandle, L"Welcome to QWB Final", 0x14u, &NumberOfCharsWritten, 0i64);
    CloseHandle(StdHandle);
    return 0164;
}