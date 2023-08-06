import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="test_password_maker",
    version="0.0.1",
    author="Sohee Han",
    author_email="eng.sohee@gmail.com",
    description="package build test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nicecoding1/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
