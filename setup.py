import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discordial",
    version="1.0.3",
    author="vcokltfre",
    author_email="vcokltfre@gmail.com",
    description="A lightweight library for Discord",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vcokltfre/discordial",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)