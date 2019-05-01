import os
import shutil
from conans import ConanFile, CMake, tools

class AmqpCppConan(ConanFile):
    name = "amqpcpp"
    version = "4.1.4"
    url = "https://github.com/CopernicaMarketingSoftware/AMQP-CPP"
    author = "l.a.r.p@yandex.ru"
    license = "Apache-2.0"
    description = "C++ library for asynchronous non-blocking communication with RabbitMQ"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "linux_tcp": [True, False]
    }
    default_options = {
        "shared": False,
        "linux_tcp": True
    }
    generators = "cmake"

    def source(self):
        git = tools.Git(folder=self.name)
        git.clone("https://github.com/CopernicaMarketingSoftware/AMQP-CPP.git")
        git.checkout("v%s" % self.version)
        os.rename(os.path.join(self.name, "CMakeLists.txt"),
                  os.path.join(self.name, "CMakeListsOriginal.txt"))
        shutil.copy("CMakeLists.txt", os.path.join(self.name, "CMakeLists.txt"))

    def requirements(self):
        self.requires.add("OpenSSL/1.0.2n@conan/stable")

    def build(self):
        cmake = CMake(self)
        cmake.definitions['AMQP-CPP_BUILD_SHARED'] = self.options.shared
        cmake.definitions['AMQP-CPP_BUILD_EXAMPLES'] = False
        if self.settings.os == "Windows":
            cmake.definitions['AMQP-CPP_LINUX_TCP'] = False
        else: cmake.definitions['AMQP-CPP_LINUX_TCP'] = self.options.linux_tcp

        cmake.configure(source_folder=self.name)
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src=os.path.join(self.name, "include"))
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["pthread"])