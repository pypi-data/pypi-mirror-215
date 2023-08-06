from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="XGen Time Series",
    version="0.1.1",
    author="Khalid OUBLAL (S2A team Institut Polytechnique de Paris)",
    author_email="khalid.oublal@polytechnique.edu",
    description="An eXplainable framework for Generative Time Series in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XgenTimeSeries/xgen-timeseries",
    project_urls={
        "Bug Tracker": "https://github.com/XgenTimeSeries/xgen-timeseries/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "numpy==1.19.4",
        "pandas==1.1.4",
        "scikit-learn==0.23.2",
        "scipy==1.5.4",
        "tqdm==4.54.0",
        "torch==1.7.0",
        "joblib==0.17.0",
        "matplotlib==3.3.3",
        "seaborn==0.11.1",
        "tensorboard==2.4.0",
    ],
    extras_require={':python_version == "3.7.*"': ["pickle5"]},
    python_requires=">=3.7",
)
