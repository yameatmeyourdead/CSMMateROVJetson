#include <iostream>
#include "Components/Drive.h"
#include <vector>
#include <signal.h>
#include <chrono>
#include <ctime>
#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif



// Create vector of components to hold all ROV parts (Global so cleanup has access to it)
std::vector<Component*> components;

void cleanup(int signum) {
    std::cout << "\n================\nStarted Cleanup" << std::endl;
    auto start = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
    for(int i = components.size()-1; i >= 0; i--) {
                components[i]->Stop(); // do any last minute cleanup on the component
                delete components[i]; // delete the component
    }
    auto end = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
    std::cout << "\nSucessfully cleaned up in " << (end-start) << " milliseconds.....exiting!\n================\n";
}

int main() {
    // catch SIGINT (control + c)
    signal(SIGINT, cleanup);

    // Create all ROV parts
    components.emplace_back(new Drive());


    // start update loop
    std::string inputBuffer;
    bool QUIT = false;
    while(!QUIT) {
        for(Component* component : components) {
                component->Update();
        }
        Sleep(2000);
    }
    
    return 0;
}