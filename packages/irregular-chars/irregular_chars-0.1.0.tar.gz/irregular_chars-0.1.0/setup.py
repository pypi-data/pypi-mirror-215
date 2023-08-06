from setuptools import find_packages, setup

setup(
    name="irregular_chars",
    version="0.1.0",
    description="A library for cleaning text, such as removing zero-width characters or converting full-width characters to half-width",
    packages=find_packages(),
    install_requires=[],
    classifiers=[  # パッケージのメタデータ（詳細は https://pypi.org/classifiers/ を参照）
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    author="Masato Emata",
    url="https://github.com/masatoEmata/replace_irregular_chars",
    keywords="",
)
