import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # Application name:
    name="travel-times-from-starting-postcode-london",
    version="0.0.1",
    author="Glaeser",
    author_email="w.glaeser@lse.ac.uk",
    description="Heatmap showing approximate travel times across London from arbitrary starting point.",
    long_description=long_description,
    packages=setuptools.find_packages(),
    url='https://github.com/wbglaeser/travel-times-london.git',
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        # Dependent packages (distributions)
    ),
    install_requires = [
    "geopy",
    "matplotlib",
    "pandas",
    "scipy",
    "numpy"]
)


