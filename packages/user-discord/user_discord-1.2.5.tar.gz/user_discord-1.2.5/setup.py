from setuptools import setup, find_packages

requirements = [
    "requests",
    "websocket-client"
]

long_description ="""### Discord
` https://discord.gg/WR9MNs5Hqv`
### How to install?
`pip install user-discord`
### No work
Join-server, login, access discord database :D"""

setup(
    name="user_discord",
    license="MIT",
    author="nxSlayer",
    version="1.2.5",
    author_email="princediscordslay@gmail.com",
    description="Library for discord bots.",
    url="https://github.com/nxSlayer/user-discord",
    packages=find_packages(),
    long_description=long_description,
    install_requires=requirements,
    keywords=[
        'user_discord',
        'user-discord',
    ],
    python_requires='>=3.6',
)