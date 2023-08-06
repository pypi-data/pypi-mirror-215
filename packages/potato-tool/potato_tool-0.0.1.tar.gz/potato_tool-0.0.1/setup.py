#!/usr/bin/env python
# coding: utf-8

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='potato_tool',
    version='0.0.1',
    author='Potato',
    author_email='ljy1058318852@163.com',
    url='https://potato.gold',
    description=u'输出染色、前置符、格式化输出及表格输出',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'terminal',
        'console',
    ],
    entry_points={
        'console_scripts': [
            'red=potato_tool:red',
            'green=potato_tool:green',
            'blue=potato_tool:blue',
            'magenta=potato_tool:magenta',
            'yellow=potato_tool:yellow',
            'cyan=potato_tool:cyan',
            'bold=potato_tool:bold',
            'Processing=potato_tool:Processing',
            'Information=potato_tool:Information',
            'Detected=potato_tool:Detected',
            'Result=potato_tool:Result',
            'Error=potato_tool:Error',
            'Input=potato_tool:Input',
            'Input_lines=potato_tool:Input_lines',
            'printF=potato_tool:printF',
            'printT=potato_tool:printT'
        ]
    }
)