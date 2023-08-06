import setuptools


with open("README.md", "r", encoding='utf-8') as readme:
    long_description = readme.read()

setuptools.setup(
    name="simulated-bifurcation",
    version="1.1.1",
    description="Efficient implementation of the quantum-inspired Simulated Bifurcation (SB) algorithm to solve Ising-like problems.",
    url="https://github.com/bqth29/simulated-bifurcation-algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8"
)