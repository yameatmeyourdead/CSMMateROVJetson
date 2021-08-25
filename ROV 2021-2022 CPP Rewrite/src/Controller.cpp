#include "Controller.h"
#include <assert.h>

Controller::Controller(short ID) {
    this->ID = ID;
    DWORD lastPacketNumber = 0;
}

void Controller::setState(const XINPUT_STATE & state) {
    this->state = state;
}

void Controller::updateController() {
    
}

ControllerHandler::ControllerHandler() {
    
}

bool ControllerHandler::isControllerConnected(DWORD i) {
    XINPUT_STATE state;
    RtlSecureZeroMemory(&state, sizeof(XINPUT_STATE)); // ensure struct's initial values are defined
    return XInputGetState(i, &state) == ERROR_SEVERITY_SUCCESS;
}

// ASSERT THAT  0 <= i <= 3
Controller* ControllerHandler::getControllerInstance(DWORD i) {
    assert(0 <= i && i <= 3);
    return controllers[i];
}

void ControllerHandler::updateControllers() {
    DWORD dwResult;
    for(DWORD i = 0; i < XUSER_MAX_COUNT; i++) {
        XINPUT_STATE state;
        RtlSecureZeroMemory(&state, sizeof(XINPUT_STATE)); // ensure struct's initial values are defined
        dwResult = XInputGetState(i, &state);
        if(dwResult == ERROR_SEVERITY_SUCCESS) {
            // specific controller is connected, update its state variable accordingly
            controllers[i]->setState(state);
        }
    }
}