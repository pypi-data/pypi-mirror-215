from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as f:
    long_description = f.read()

setup(
    name="images-compare",
    version="0.5.0",
    description="This Python package allows for image comparison between two provided images using a specified threshold",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/denzilrdz/images-compare",
    author="Denzil Rodrigues",
    author_email="denzil.rdz@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy>=1.25.0", "opencv-python>=4.7.0.72"],
    extras_requires={"dev": ["twine>=4.0.2"]},
    python_requires=">=3.11",
)
