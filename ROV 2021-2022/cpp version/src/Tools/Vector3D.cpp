#include "Vector3D.h"

double Vector3D::getI(){
    return this->i;
}

double Vector3D::getJ(){
    return this->j;
}

double Vector3D::getK(){
    return this->k;
}

double* Vector3D::getComponents() {
    double* toRet = new double[3];
    toRet[0] = this->i;
    toRet[1] = this->j;
    toRet[2] = this->k;
    return toRet;
}

void Vector3D::setComponents(double i, double j, double k) {
        this->i = i;
        this->j = j;
        this->k = k;
    }

void Vector3D::setComponents(double ijk[3]) {
    this->i = ijk[0];
    this->j = ijk[1];
    this->k = ijk[2];
}

double Vector3D::magnitude() {
    return sqrt(pow(this->i,2) + pow(this->j, 2) + pow(this->k, 2));
}

Vector3D Vector3D::cross(Vector3D other) {
    return Vector3D(j*other.k - k*other.j, k*other.i - i*other.k, i*other.j - j*other.i);
}

double Vector3D::dot(Vector3D other) {
    return (i * other.i) + (j * other.j) + (k * other.k);
}