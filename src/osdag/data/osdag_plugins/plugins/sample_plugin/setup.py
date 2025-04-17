from setuptools import setup, find_packages

setup(
    name="osdag-sample-plugin",
    version="1.0.0",
    description = "sample plugin"
    author="Aathithya Sharan",
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.14.2',
    ],
    entry_points={
        "osdag.plugins": [
            "sample_plugin = sample_plugin.plugin:SamplePlugin"
        ]
    },
    python_requires=">=3.7",
) 