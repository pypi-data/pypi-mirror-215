import os
from os.path import join
from setuptools import setup, Extension
from Cython.Build import cythonize


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'Programming Language :: Python :: 3',
]


directory_path = os.path.dirname(
    os.path.abspath(__file__)
    )

ext_data = {
    'pythonce.ola.wrap_ola': {
        'sources': [
            join(directory_path, 'pythonce', 'ola', 'wrap_ola.pyx'),
            join(directory_path, 'pythonce', 'ola', 'ola.c')]
    },
    'pythonce.calculator.cal': {
        'sources': [
            join(directory_path, 'pythonce', 'calculator', 'cal.pyx')]}
}


extensions = []

for name, data in ext_data.items():

    sources = data['sources']
    include = data.get('include', [])

    obj = Extension(
        name,
        sources=sources,
        include_dirs=include
    )
    
    extensions.append(obj)


# Use cythonize on the extension object.
setup(
    name='pythonce',
    version='0.0.7',
    description='Python Library writen in C ',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='carlinhoshk',
    author_email='carlosmdohk@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='c',
    install_requires=[
        ''
    ],
    #package_dir={'pythonce': ''},
    ext_modules=cythonize(extensions)
    )