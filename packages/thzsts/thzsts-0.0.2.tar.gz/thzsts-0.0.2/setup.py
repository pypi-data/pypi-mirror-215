from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='thzsts',
    version='0.0.2',
    description='Function to perform THz STS algorithm and simulate measurements.',
    license='MIT',
    py_modules=['thzstsalgorithm', 'thzccsim'],
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NanoTHzCoding/THz_STS_Algorithm",
    author="Stefanie Adams",
    author_email="nanothz.coding@gmail.com",
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "scikit-learn"
    ],
)
     