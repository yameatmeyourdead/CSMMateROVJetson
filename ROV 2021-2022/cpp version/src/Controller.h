#include <xinput.h>
#include <map>
#include <string>

// add a layer of abstraction between code and XInput's terribleness
class Controller {
public:
    Controller(short ID);

    void updateController();
    std::map<std::string, bool> getPresses(); // return representation of this controller's state

    BYTE getBatteryInformation();
    void setState(const XINPUT_STATE& state);
private:
    short ID;
    DWORD lastPacketNumber;
    XINPUT_STATE state;
    std::map<std::string, bool> buttons;
    std::map<std::string, float> sticksAndTriggers;
};

class ControllerHandler {
public:
    ControllerHandler();
    ~ControllerHandler();

    bool isControllerConnected(DWORD i);
    Controller* getControllerInstance(DWORD i);
    void updateControllers();
protected:

private:
    Controller* controllers [4] = {new Controller(0), new Controller(1), new Controller(2), new Controller(3)};;
};