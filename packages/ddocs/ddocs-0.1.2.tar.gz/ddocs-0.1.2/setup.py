from setuptools import find_packages, setup

setup(
    name='ddocs',
    packages=find_packages(include=["ddocs"]),
    package_dir= {'ddocs': 'ddocs'},
    package_data= {'ddocs': ['languages/*', 'fonts/*']},
    entry_points={"console_scripts": [
        "ddocs=ddocs.__main__:main",
        "ddocs-gui = ddocs.gui:main",
        ]
    },
    version='0.1.0',
    description='Offline and fast documentation (+ source code) cli viewer for python libraries.',
    author='gkegke',
    license='MIT',
    install_requires=[
        "dearpygui",
        "platformdirs"
    ],
    extras_require={
        "dev": ["pytest"]
    },
    tests_require=["pytest"],
    python_requires=">=3.8",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    project_urls={
        "Homepage": "https://github.com/gkegke/ddocs"
    },
)
