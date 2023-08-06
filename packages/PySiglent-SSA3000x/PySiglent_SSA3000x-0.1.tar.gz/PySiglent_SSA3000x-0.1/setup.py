from setuptools import setup, find_packages
import json


version_file = '_INTERNAL_version.json'
project_name = 'PySiglent_SSA3000x'
external_modules = ('pyvisa','numpy')

ver_data = json.load(open(version_file, 'r'))
local_build_version = ver_data['build']['ver']

setup(
    name=project_name,
    version=local_build_version,
    packages=find_packages(exclude=('_INTERNAL_build.py',
                                    '_INTERNAL_version.json',
                                    '.gitignore',
                                    'workspace.code-workspace',
                                    'tests.py')),
    url="https://github.com/Minu-IU3IRR/PySiglent_SSA3000x",
    bugtrack_url = 'https://github.com/Minu-IU3IRR/PySiglent_SSA3000x/issues',
    license='MIT',
    author='Manuel Minutello',
    description='module to easily contorl a Siuglent SSA3000x sieries spectrum analyzer and quickly build a measurement setup',
    long_description=open('README.md').read(),
    install_requires=external_modules,
    python_requeres = '>=3.6'
)