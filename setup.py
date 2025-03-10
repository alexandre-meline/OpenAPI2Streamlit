from setuptools import setup, find_packages

setup(
    name="openapi2streamlit",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openapi-parser",
    ],
    entry_points={
       "console_scripts": [
           "openapi2streamlit=openapi2streamlit.main:main",
       ],
   },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
