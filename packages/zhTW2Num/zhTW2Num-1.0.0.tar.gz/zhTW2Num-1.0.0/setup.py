import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="zhTW2Num",
    version="1.0.0",
    author="ben60523",
    description="Convert zh-TW numbers to Arabic numerals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["zhTW2Num"],
    package_dir={'':'.'},
    install_requires=[]
)
