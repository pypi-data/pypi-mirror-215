from setuptools import setup

# Build command: python setup.py sdist
# Upload command: twine upload dist/*

setup(
    name = 'spoutlang',
    version = '0.2.1',
    author = 'Tasfiqul Tapu',
    author_email = 'iamtasfiqultapu@gmail.com',
    license = 'MIT',
    description = 'An interpreted programming language aimed at demistifying bit manipulation.',
    url = 'https://github.com/TasfiqulTapu/spout',
    py_modules = ['main', 'spout'],
    install_requires = [],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        spout=main:main
    '''
)