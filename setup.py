from setuptools import find_packages, setup

setup(
    name="climate_qa",
    version="0.1",
    packages=find_packages(),
    author="Daniel Liden",
    author_email="djliden91@gmail.com",
    description="A Python package for querying and summarizing major climate change documents",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/djliden/climate_qa",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',  # Update with your project's Python version requirement
    install_requires=["numpy", "openai", "pandas", "pypdf", "requests",
                      "sentence_transformers", "setuptools", "streamlit",
                      "python-dotenv",
    ],
)
