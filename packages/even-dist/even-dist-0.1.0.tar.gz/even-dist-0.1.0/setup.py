from setuptools import find_packages, setup

setup(
    name="even-dist",
    packages=find_packages(include=["even_dist"]),  # I only will upload this package
    version="0.1.0",
    description="My first Python library",
    install_requires=["numpy", "matplotlib"],
    author="kirp",
    author_email="kirp@umich.edu",
    license="MIT",
    setup_requires=["pytest-runner"],
    tests_require=["pytest==4.4.1"],
    test_suite="tests",
)
