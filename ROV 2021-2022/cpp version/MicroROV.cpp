#include "Component.hpp"
#include <iostream>

class MicroROV : public Component {
public:
    MicroROV() {

    }

    ~MicroROV() {

    }

    virtual void update() {
        std::cout << "MicroROV Update" << '\n';
    }
};