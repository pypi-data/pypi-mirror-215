from setuptools import setup

setup(
    name='hi-cli-jash',
    version='0.1.2',
    description='A simple CLI tool that prints "Hi"',
    py_modules=['hi'],
    entry_points={
        'console_scripts': [
            'hi=hi:say_hi',
        ],
    },
    author='jashwanth peddisetty',
    author_email='jashwanth0712@gmail.com',
)
