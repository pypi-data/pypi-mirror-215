from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="testless_autocomplete",
    version="0.0.110",
    description="Auto Complete Package",
    package_data={
        '../Auto_Complete': ['Auto_Complete/*'],
    },
    package_dir={"": "../Auto_Complete/Auto_Complete"},
    packages=find_packages(where="../Auto_Complete/Auto_Complete"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="TestLess",
    zip_safe=False,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["bson >= 0.5.10"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    
)
