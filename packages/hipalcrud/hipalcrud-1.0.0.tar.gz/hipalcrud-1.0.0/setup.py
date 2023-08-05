from setuptools import find_packages, setup

setup(
    name="hipalcrud",
    version="1.0.0",
    description="Libreria para crud basica.",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pydantic==1.10.7",
        "sqlalchemy==2.0.15",
        "fastapi==0.95.0",
    ],
    url="http://git.hipal.com.co/libraries/ms-mixins/-/tree/feature/mixins",
    author="Hipal",
    author_email="desarrollo@hipal.com.co",
)
