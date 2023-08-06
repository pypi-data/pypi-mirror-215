import setuptools
from splinterglyph.VERSION import version

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="splinterglyph",
    version=version,
    scripts=["splinterglyph_encrypt", "splinterglyph_decrypt"],
    author="Bill Bradley",
    description="A tool for encrypting and decrypting files using distributed keys",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mirabolic/splinterglyph",
    packages=setuptools.find_namespace_packages(),
    install_requires=["pycryptodome>=3.18.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=["setuptools_scm"],
)
