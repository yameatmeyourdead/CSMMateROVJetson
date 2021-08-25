// Defines abstract base class and pure virtual methods for all components of the ROV
class Component{
public:
    virtual void Update() = 0;
    virtual void AutoUpdate() = 0;
    virtual void Stop() = 0;
protected:

private:

};