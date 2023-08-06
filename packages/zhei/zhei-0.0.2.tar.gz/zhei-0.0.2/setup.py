#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='zhei',
    version='0.0.2',
    author='deng1fan',
    author_email='dengyifan@iie.ac.cn',
    url='https://github.com/deng1fan',
    description=u'深度学习实验工具类',
    packages=find_packages(),
    install_requires=[],  # 依赖列表
    exclude=["*.tests", "*.tests.*", "tests"],
    include_package_data=True,
    python_requires='>=3.6',
)
