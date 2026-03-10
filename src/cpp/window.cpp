#include "window.h"

Window::Window(int w, int h)
{
    SDL_Init(SDL_INIT_VIDEO);

    window = SDL_CreateWindow(
        "PyVerse",
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        w,
        h,
        SDL_WINDOW_SHOWN
    );
}

Window::~Window()
{
    destroy();
}

void Window::show()
{
    if (window)
        SDL_ShowWindow(window);
}

void Window::destroy()
{
    if (window) {
        SDL_DestroyWindow(window);
        window = nullptr;
    }
    SDL_Quit();
}