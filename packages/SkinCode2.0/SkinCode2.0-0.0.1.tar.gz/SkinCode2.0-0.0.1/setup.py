import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SkinCode2.0",
    version="0.0.1",
    author="Lisa Simon",
    author_email="l.simon@stud.macromedia.de",
    description="SkinCode2.0 package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lisa-smn/SkinCode2.0",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/SkinCode2.0/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)

