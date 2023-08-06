import pathlib
import sys
from setuptools import setup


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

# make sure that
# ref https://pybind11.readthedocs.io/en/stable/compiling.html#copy-manually
# and https://zhuanlan.zhihu.com/p/463176808
ext_modules = []
try:
    from pybind11.setup_helpers import Pybind11Extension
    args = ["-O2"] if sys.platform == "win32" else ["-O3", "-std=c++14", "-g", "-Wno-reorder"]
    ext_modules = [
        Pybind11Extension(
            name="fast_coco_eval.fast_coco_eval",
            sources=['fast_coco_eval/cocoeval/cocoeval.cpp'],
            extra_compile_args=args
        ),
    ]
except ImportError:
    pass

setup(
    name='fast-coco-eval-python',
    version='0.0.2',
    author='Mark-ZhouWX',
    author_email='zhouwuxing@qq.com',
    license='Apache License 2.0',
    description='fast coco eval api',
    long_description=long_description,
    ext_modules=ext_modules,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"],
    url="https://github.com/Mark-ZhouWX/fast-coco-eval",
    setup_requires=["pybind11"],
    install_requires=["pybind11", "pycocotools"],
    packages=["fast_coco_eval"],
    package_data={"fast_coco_eval": ["cocoeval/*.h"]}
)
