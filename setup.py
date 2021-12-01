from setuptools import setup

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="nextcord-tortoise",
    author="pmdevita",
    packages=["nextcord_tortoise"],
    license="MIT",
    description="Database integration for Nextcord with Tortoise-ORM",
    install_requires=requirements,
    python_requires='>=3.8.0',
    version="0.1a"
)

