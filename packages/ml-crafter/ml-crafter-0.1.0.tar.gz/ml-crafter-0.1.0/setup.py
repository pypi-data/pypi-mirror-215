import setuptools

setuptools.setup(
    name='ml-crafter',
    version='0.1.0',
    description='Performs end to end ML model development',
    packages=setuptools.find_packages(),
    install_requires=[ "numpy",
        "scipy",
        # List your package dependencies here
    ],
)
