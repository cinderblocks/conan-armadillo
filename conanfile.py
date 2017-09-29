from conans import ConanFile, CMake, tools
import os

class ArmadilloConan(ConanFile):
    name = "Armadillo"
    version = "8.100.1"
    license = "http://arma.sourceforge.net/license.html"
    url = "https://github.com/cinderblocks/conan-armadillo"
    description = "Armadillo is a high quality linear algebra library (matrix maths) for the C++ language, aiming towards a good balance between speed and ease of use"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports_sources = "ARMA_FindOpenBLAS.cmake"
    source_archive = "http://sourceforge.net/projects/arma/files/armadillo-%s.tar.xz" % version

    def requirements(self):
        self.requires("OpenBLAS/0.2.20@slidewave/stable")

    def source(self):
        self.output.info("Downloading %s" % self.source_archive)
        tools.download(self.source_archive, "armadillo.tar.xz")        
        tools.check_sha256("armadillo.tar.xz", "54773f7d828bd3885c598f90122b530ded65d9b195c9034e082baea737cd138d")
        self.run("cmake -E tar xf armadillo.tar.xz")
        os.unlink("armadillo.tar.xz")
        # Copy Conan compatible FindOpenBLAS in place of Armadillo's
        self.run("cp -v ARMA_FindOpenBLAS.cmake armadillo-8.100.1/cmake_aux/Modules")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("armadillo-%s/CMakeLists.txt" % self.version, "project(armadillo CXX C)", '''project(armadillo CXX C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def config_options(self):
        # Armadillo warns shared lib doesn't work on MSVC
        if self.settings.compiler == "Visual Studio":
            self.options.shared = False

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        self.run('cmake armadillo-8.100.1 %s' % cmake.command_line)
        #self.run("cmake --build . %s" % cmake.build_config)
        cmake.build(target="install")

    def package(self):
        self.copy("*.h", dst="include", src="armadillo")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["armadillo"]
        # FIXME need linux and macOS
        if self.settings.os == "Windows":
            suffix = ""
            if self.settings.arch == "x86_64":
                suffix += "Win64_"   
            suffix += str(self.settings.compiler.runtime)
            self.cpp_info.libs += ["blas_" + suffix, "lapack_" + suffix]
