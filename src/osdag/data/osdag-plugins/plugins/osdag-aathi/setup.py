from setuptools import setup, find_packages

setup(
    name="osdag-aathi",
    version="1.0.0",
    description="test plugin",
    author="Aathithya Sharan",
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.14.2',
    ],
    entry_points={
        "osdag.plugins": [
            "aathi = aathi_plugin.plugin:AathiPlugin"
        ]
    },
    python_requires=">=3.7",
) 
