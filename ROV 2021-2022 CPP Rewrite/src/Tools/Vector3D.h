#include <math.h>

class Vector3D {
public:
    Vector3D(double i, double j, double k) {
        this->i = i;
        this->j = j;
        this->k = k;
    }
    ~Vector3D(){};

    double getI();
    double getJ();
    double getK();
    double* getComponents();

    void setComponents(double i, double j, double k);
    void setComponents(double ijk[3]);
    double magnitude();
    Vector3D cross(Vector3D other);
    double dot(Vector3D other);
protected:

private:
    double i = 0.0f;
    double j = 0.0f;
    double k = 0.0f;
};