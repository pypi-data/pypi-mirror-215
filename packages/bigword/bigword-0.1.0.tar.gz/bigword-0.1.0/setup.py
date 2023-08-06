from setuptools import setup, find_packages

setup(
    name="bigword",
    version="0.1.0",
    description="Print big words on a grid",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Casey Webb",
    url="https://github.com/caseyrwebb/bigword",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "bigword=bigword.__main__:bigword",
        ],
    },
    python_requires=">=3.10.5",
    install_requires=[],
)
