#include <pybind11/pybind11.h>
#include <SDL.h>

namespace py = pybind11;

SDL_Window* window = nullptr;

void create_window(int w, int h) {
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

void destroy_window() {
    if (window) {
        SDL_DestroyWindow(window);
        window = nullptr;
    }
    SDL_Quit();
}

PYBIND11_MODULE(pyverse, m) {
    m.def("create_window", &create_window);
    m.def("destroy_window", &destroy_window);
}