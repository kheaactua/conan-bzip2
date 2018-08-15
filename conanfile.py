#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

from conans import CMake, tools
from conans import ConanFile


class Bzip2Conan(ConanFile):
    name = "bzip2"
    version = "1.0.6"
    branch = "master"
    generators = "cmake"
    settings = "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    exports = ["CMakeLists.txt"]
    url = "https://github.com/lasote/conan-bzip2"
    license = "BSD-style license"
    description = "bzip2 is a freely available, patent free (see below), high-quality data " \
                  "compressor. It typically compresses files to within 10% to 15% of the best" \
                  " available techniques (the PPM family of statistical compressors), whilst " \
                  "being around twice as fast at compression and six times faster at decompression."

    requires = 'helpers/0.3@ntc/stable'

    @property
    def zip_folder_name(self):
        return "bzip2-%s" % self.version

    def config(self):
        del self.settings.compiler.libcxx

    def source(self):
        zip_name = "bzip2-%s.tar.gz" % self.version

        from source_cache import copyFromCache
        if not copyFromCache(zip_name):
            tools.download("http://www.bzip.org/%s/%s" % (self.version, zip_name), zip_name)
        tools.check_md5(zip_name, "00b516f4704d4a7cb50a1d97e6e8e15b")
        tools.unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        shutil.move("CMakeLists.txt", "%s/CMakeLists.txt" % self.zip_folder_name)
        with tools.chdir(self.zip_folder_name):
            os.mkdir("_build")
            with tools.chdir("_build"):
                cmake = CMake(self)
                if self.options.fPIC:
                    cmake.definitions["FPIC"] = "ON"
                cmake.configure(build_dir=".", source_dir="..")
                cmake.build(build_dir=".")

    def package(self):
        self.copy("*.h", "include", "%s" % self.zip_folder_name, keep_path=False)
        self.copy("*bzip2", dst="bin", src=self.zip_folder_name, keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=self.zip_folder_name, keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src=self.zip_folder_name, keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="%s/_build" % self.zip_folder_name, keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="%s/_build" % self.zip_folder_name, keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src="%s/_build" % self.zip_folder_name, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['bz2']

# vim: ts=4 sw=4 expandtab ffs=unix ft=python foldmethod=marker :
