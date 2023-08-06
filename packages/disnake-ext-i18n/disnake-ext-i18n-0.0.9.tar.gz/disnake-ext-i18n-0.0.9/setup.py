from setuptools import setup
from re import search, MULTILINE

pkg_name = "i18n"
prj_path = "disnake/ext/{}/".format(pkg_name)
prj_name = "disnake-ext-{}".format(pkg_name)
descriptors = ("./README.md",)
long_description = ""
version = "0.0.9"

for desc in descriptors:
    with open(desc, encoding="utf-8") as f:
        long_description += f.read()

setup(
    name=prj_name,
    version=version,
    description="A fork of the Pycord extension to support automatic text translations in 107 languages to also support Disnake.",
    author="Rickaym",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jaymart95/{}".format(prj_name),
    project_urls={
        "Issue tracker": "https://github.com/jaymart95/{}/issues".format(prj_name),
    },
    license="MIT",
    python_requires=">=3.7",
    packages=[prj_path.replace("/", ".", -1)],
    install_requires=["disnake>=2.7.0", "googletrans==3.1.0a0"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.10",
    ],
)
