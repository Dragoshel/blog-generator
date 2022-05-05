from setuptools import setup

setup(
    name="Api",
    packages=["Authentication", "Core", "Builder"],
    include_package_data=True,
    install_requires=[
        "flask",
    ]
)
