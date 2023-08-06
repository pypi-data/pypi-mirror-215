from setuptools import setup, find_packages

DESCRIPTION = 'Hardy-Weinberg Equilibrium Calculator. Calculates the expected genotype frequencies based on the ' \
              'allele frequencies of a population in Hardy-Weinberg equilibrium.'

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

with open("requirements.txt", "r") as fh:
    REQUIREMENTS = fh.read()

with open("LICENSE", "r") as fh:
    LICENSE = fh.read()

with open("VERSION", "r") as fh:
    VERSION = fh.read()

setup(
    name="hardyweinbergcalculator",
    # Do Not Change This Line
    version=VERSION,
    author="Dellius Alexander",
    author_email="info@hyfisolutions.com",
    maintainer="info@hyfisolutions.com",
    maintainer_email="info@hyfisolutions.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/dellius-alexander/Hardy-Weinberg.git",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*", "dist", "build", "logs"]),
    license=LICENSE,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",

        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    package_data={
        "src": ["data/*.*"]
    },
    package_dir={
        "hardy_weinberg": "src"
    },
    entry_points={
        "console_scripts": [
            "hwc = src.__main__:main"
        ]
    },
    python_requires=">=3.7",
    include_package_data=True,
    zip_safe=False,
    install_requires=[REQUIREMENTS],
    keywords=[
        "hardy-weinberg-equilibrium",
        "hardy-weinberg-equilibrium-calculator",
        "hardy-weinberg-calculator",
        "chi-square",
        "chi-square-test"
    ]
)
