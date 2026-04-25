#include <dlfcn.h>

#include <cstdlib>
#include <iostream>
#include <string>

int main(int argc, char** argv)
{
    if (argc != 2) {
        std::cerr << "Usage: test_plugin_loader <plugin.so>\n";
        return EXIT_FAILURE;
    }

    const std::string plugin_path = argv[1];

    void* handle = dlopen(plugin_path.c_str(), RTLD_NOW | RTLD_LOCAL);
    if (handle == nullptr) {
        std::cerr << "dlopen failed for '" << plugin_path << "':\n"
                  << dlerror() << "\n";
        return EXIT_FAILURE;
    }

    dlerror(); // clear old error state

    void* symbol = dlsym(handle, "LibTokaMapFactoryLoader");
    const char* error = dlerror();

    if (error != nullptr || symbol == nullptr) {
        std::cerr << "dlsym failed for LibTokaMapFactoryLoader:\n"
                  << (error ? error : "symbol was null") << "\n";
        dlclose(handle);
        return EXIT_FAILURE;
    }

    std::cout << "Loaded plugin and found LibTokaMapFactoryLoader\n";

    dlclose(handle);
    return EXIT_SUCCESS;
}
