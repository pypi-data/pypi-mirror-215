from setuptools import setup, find_packages

setup(
    name="cryptoowl",
    version="0.0.1",
    author="Cryptoowl",
    author_email="cryptoowl.app@gmail.com",
    description="A library, where you store common codes for different modules for cryptoowl",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["time"],
)
