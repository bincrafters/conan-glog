#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class GlogConan(ConanFile):
    name = "glog"
    version = "0.4.0"
    url = "https://github.com/bincrafters/conan-glog"
    homepage = "https://github.com/google/glog"
    description = "Google logging library"
    license = "BSD-3-Clause"
    topics = ("conan", "glog", "logging", "google", "log")
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
            del self.options.fPIC
        if self.options.with_gflags:
            self.options["gflags"].nothreads = False

    def requirements(self):
        self.requires("libunwind/1.3.1@bincrafters/stable")
        if self.options.with_gflags:
            self.requires("gflags/2.2.2@bincrafters/stable")

    def source(self):
        sha256 = "f28359aeba12f30d73d9e4711ef356dc842886968112162bc73002645139c39c"
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['WITH_GFLAGS'] = self.options.with_gflags
        cmake.definitions['WITH_THREADS'] = self.options.with_threads
        cmake.definitions['BUILD_TESTING'] = False
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("COPYING", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(['pthread', 'm'])
