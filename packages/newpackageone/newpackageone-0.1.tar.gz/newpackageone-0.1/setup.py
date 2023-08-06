from setuptools import setup

setup(
    name='newpackageone',
    version='0.1',
    description='My Python Package',
    py_modules=['newpackageone'],
    entry_points={
        'console_scripts': [
            'newpackageone = newpackageone:greet'
        ]
    },
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
