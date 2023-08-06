import os
import bump
from setuptools import setup, find_packages


with open(os.path.join(os.path.dirname(__file__), "README.md")) as fh:
    long_description = fh.read()


requirements = [
    "Markdown",
    "python-dotenv",
    "Requests",
    "mdx_truly_sane_lists",
    "markdown_link_attr_modifier",
    "click",
]

setup(
    name="local-first-tistory",
    version="0.0.2",
    author="Kangjae Choi",
    author_email="choikj33@gmail.com",
    description="It will help you to manage locally saved markdown \
            to upload to Tistory",
    license="MIT",
    keywords="tistory terminal markdown image",
    url="https://github.com/choikangjae/local-first-tistory",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    entry_points={"console_scripts": ["tistory=src.tistory:cli"]},
    classifiers=[
        "Operating System :: POSIX",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
        "Topic :: Terminals",
        "License :: OSI Approved :: MIT License",
    ],
)
