#!/usr/bin/env python
# coding: utf-8

import setuptools
import codecs

with codecs.open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='potato_tool',
    version='0.0.5',
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
        'wcwidth'
    ],
    entry_points={
        'console_scripts': [
            'p=potato_tool:p'
            'clear=potato_tool:clear'
            'red=potato_tool:red',
            'redP=potato_tool:redP',
            'green=potato_tool:green',
            'greenP=potato_tool:greenP',
            'blue=potato_tool:blue',
            'blueP=potato_tool:blueP',
            'magenta=potato_tool:magenta',
            'magentaP=potato_tool:magentaP',
            'yellow=potato_tool:yellow',
            'yellowP=potato_tool:yellowP',
            'cyan=potato_tool:cyan',
            'cyanP=potato_tool:cyanP',
            'bold=potato_tool:bold',
            'boldP=potato_tool:boldP',
            'Processing=potato_tool:Processing',
            'ProcessingP=potato_tool:ProcessingP',
            'Information=potato_tool:Information',
            'InformationP=potato_tool:InformationP',
            'Detected=potato_tool:Detected',
            'DetectedP=potato_tool:DetectedP',
            'Result=potato_tool:Result',
            'ResultP=potato_tool:ResultP',
            'Error=potato_tool:Error',
            'ErrorP=potato_tool:ErrorP',
            'Input=potato_tool:Input',
            'InputP=potato_tool:InputP',
            'Input_lines=potato_tool:Input_lines',
            'printF=potato_tool:printF',
            'pF=potato_tool:pF',
            'printT=potato_tool:printT',
            'pT=potato_tool:pT',
            'listPT=potato_tool:listPT',
            'logo_1=potato_tool:logo_1'
            'logo_2=potato_tool:logo_2'
        ]
    }
)