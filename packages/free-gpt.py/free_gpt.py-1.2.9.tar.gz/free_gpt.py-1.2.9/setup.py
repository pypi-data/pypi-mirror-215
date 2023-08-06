from setuptools import setup, find_packages

requirements = [
    "requests"
]

long_description ="""### Discord
` https://discord.gg/WR9MNs5Hqv`
### How to install?
`pip install free_gpt.py`
### How Workd"""

setup(
    name="free_gpt.py",
    license="MIT",
    author="nxSlayer",
    version="1.2.9",
    author_email="princediscordslay@gmail.com",
    description="Library for use free gpt 3.5 in python",
    url="https://github.com/nxSlayer/free_gpt",
    packages=find_packages(),
    long_description=long_description,
    install_requires=requirements,
    keywords=[
        'free_gpt'
    ],
    python_requires='>=3.6',
)