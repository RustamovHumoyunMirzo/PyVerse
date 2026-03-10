#pragma once
#include <SDL.h>

class Window {
public:
    Window(int w, int h);
    ~Window();

    void show();
    void destroy();

private:
    SDL_Window* window;
};