#include <string>
#pragma once // ensure this class is only defined once

// Abstract base class of every programmable part on ROV
class Component {
public:
    // Constructor / Destructor
    Component(){};
    ~Component(){};
    // virtual (not pure) update function
    virtual void update(){return;};
};