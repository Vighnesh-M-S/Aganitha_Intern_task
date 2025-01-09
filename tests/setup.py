from setuptools import setup, find_packages

setup(
    name="get-papers",
    version="0.1.0",
    description="A tool to fetch and process PubMed papers.",
    author="VIGHNESH M S",
    author_email="vighneshms21@gmail.com",
    packages=find_packages(),
    install_requires=["requests", "pandas"],
    entry_points={
        "console_scripts": [
            "get-papers=scripts.get_papers:main"
        ]
    }
)