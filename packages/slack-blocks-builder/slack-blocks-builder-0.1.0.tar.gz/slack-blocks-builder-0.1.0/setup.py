# noqa=D100
# type: ignore
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

meta = {}
with open("src/blocks_builder/version.py", encoding="utf-8") as f:
    exec(f.read(), meta)

setup(
    name="slack-blocks-builder",
    version=meta["__version__"],
    desciption="Build Slack block kit blocks from YAML and JSON files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/ABizzinotto/slack-blocks-builder",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=["pydantic", "pyyaml"],
    entry_points={"console_scripts": ["generate_sample_files=blocks_builder.generate_files:generate_sample_files"]},
)
