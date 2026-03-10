#include "app.h"
#include <SDL.h>

namespace py = pybind11;

void run_engine(py::object app)
{
    auto emit = app.attr("emit");

    emit("launch");

    bool running = true;

    while (running)
    {
        SDL_Event e;

        while (SDL_PollEvent(&e))
        {
            if (e.type == SDL_QUIT)
            {
                emit("quit");
                running = false;
            }
        }

        emit("update");
    }
}