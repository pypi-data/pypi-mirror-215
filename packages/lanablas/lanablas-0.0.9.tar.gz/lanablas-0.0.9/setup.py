import os
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


class CustomBuildExt(build_ext):
    def build_extension(self, ext):
        # Set the library_dirs and runtime_library_dirs to use the local openblas/lib directory
        ext.library_dirs.append(os.path.join(directory, 'openblas', 'lib'))
        ext.runtime_library_dirs.append(os.path.join(directory, 'openblas', 'lib'))
        super().build_extension(ext)


module_extension = Extension(
    'matrix',
    sources=['lanablas/matrix.c'],
    libraries=['openblas'],  # Link against the BLAS library
    extra_compile_args=['-std=c11'],
    include_dirs=['openblas/include'],  # BLAS include directory within your package
)

setup(
    name='lanablas',
    version='0.0.9',
    description='Extension module for matrix multiplication',
    author='Marco Salvalaggio',
    author_email='mar.salvalaggio@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['lanablas'],
    package_data={
        'lanablas': ['openblas/*'],  # Include all files within the openblas directory
    },
    ext_modules=[module_extension],
    cmdclass={'build_ext': CustomBuildExt},  # Use the custom build_ext command
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
