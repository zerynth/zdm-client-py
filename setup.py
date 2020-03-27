import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "paho-mqtt",
    "click"
]

setuptools.setup(
    name="zdm-client-py",
    version="0.0.3",
    author="Zerynth Team",
    author_email="d.neri@zerynth.com",
    description="ZDM Client Python Library",
    long_description=long_description + '\n\n' + history,
    long_description_content_type="text/markdown",
    url="https://github.com/zerynth/zdm-client-py.git",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    include_package_data=True
)
