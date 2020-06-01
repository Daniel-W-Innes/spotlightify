from setuptools import setup, find_packages

setup(
    name='spotlightify',
    version='2020.5.31.1',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    url='https://github.com/spotlightify/spotlightify',
    include_package_data=True,
    install_requires=['PyQt5~=5.14.2', 'pynput~=1.6.8', 'spotipy~=2.12.0', 'setuptools~=47.1.1', 'requests~=2.23.0'],
    setup_requires=['wheel'],
    classifiers=['Development Status :: 4 - Beta', "Programming Language :: Python :: 3"],
    entry_points={'console_scripts': ['spotlightify=spotlightify.app:main']}
)
