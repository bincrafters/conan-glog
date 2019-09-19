#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class GlogConan(ConanFile):
    name = "glog"
    version = "20181109"
    url = "https://github.com/bincrafters/conan-glog"
    homepage = "https://github.com/google/glog/"
    description = "Google logging library"
    license = "BSD 3-Clause"
    author = "Bincrafters <bincrafters@gmail.com>"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "with_gflags": [True, False], "with_threads": [True, False]}
    default_options = {'shared': False, 'fPIC': True, 'with_gflags': True, 'with_threads': True}
    _source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def requirements(self):
        if self.options.with_gflags:
            self.requires("gflags/2.2.2@bincrafters/stable")
        
    def source(self):
        commit = "5c292672df04ab82a97be5116d47dc0cc544b39f"
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, commit))
        extracted_dir = self.name + "-" + commit
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['WITH_GFLAGS'] = self.options.with_gflags
        cmake.definitions['WITH_THREADS'] = self.options.with_threads
        cmake.definitions['BUILD_TESTING'] = False
        cmake.configure()
        return cmake

    def build(self):
        if self.options.with_gflags:
            tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"), "gflags 2.2.0", "gflags 2.2.1 REQUIRED CONFIG")
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("COPYING", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append('pthread')
