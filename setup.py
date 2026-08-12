from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="text-analyzer",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Professional text analysis tool with advanced features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Raf150z/text-analyzer",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pytest>=7.0.0",
    ],
    extras_require={
        "dev": [
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "sphinx>=4.5.0",
        ],
        "viz": [
            "matplotlib>=3.5.0",
            "wordcloud>=1.8.0",
        ],
    },
)