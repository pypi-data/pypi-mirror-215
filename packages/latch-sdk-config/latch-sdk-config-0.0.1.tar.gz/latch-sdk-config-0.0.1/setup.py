from setuptools import find_packages, setup

setup(
    name="latch-sdk-config",
    version="v0.0.1",
    author_email="ayush@latch.bio",
    description="Configuration for the Latch SDK",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8,<3.11",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
