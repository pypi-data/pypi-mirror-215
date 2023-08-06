from setuptools import setup, find_packages

setup(
    name='PyPokerEngineWheel',
    version='1.0.1',
    author='derthek',
    author_email='shape07_mrm@hotmail.com',
    description='Poker engine for poker AI development in Python ',
    license='MIT',
    keywords='python poker emgine ai',
    url='https://github.com/ishikota/PyPokerEngine',
    packages=[pkg for pkg in find_packages() if pkg != "tests"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
    ],
)
