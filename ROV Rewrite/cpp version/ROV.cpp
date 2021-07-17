#include "Component.hpp"
#include "Drive.cpp"
#include "Manipulator.cpp"
#include "MicroROV.cpp"
#include <iostream>
#include <vector>

#include <opencv2/opencv.hpp>

// Create Linked List of Components
std::vector<Component*> components;

void initialize() {
    // initialize every part of robot here
    components.emplace_back(new Drive());
    components.emplace_back(new Manipulator());
    components.emplace_back(new MicroROV());
}

// Main Robot Loop
int main() {
    // initialize the robot
    initialize();

    // update components
    // forever loop
    while(false) {
        // update each component
        for(Component* component : components) {
            component->update();
        }
    }
    
    std::string img = "assets\\pickle zacx.png";
    cv::Mat srcImage = cv::imread(img);
    cv::imshow("srcImage", srcImage);
    cv::waitKey(0);
    return 0;
}