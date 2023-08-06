from setuptools import setup

with open("requeriments.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="trimnet",
    version="1.0.1",
    description="Your library description",
    author="Your Name",
    packages=["trimnet_drug"],
    install_requires=requirements + [
        "torch",
        "torchvision",
        "torchaudio",
    ],
)
