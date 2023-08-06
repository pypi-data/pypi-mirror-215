from setuptools import setup

setup(
    name='printarg',
    version='1.0',
    py_modules=['print_arg'],
    entry_points={
        'console_scripts': [
            'printarg = print_arg:main'
        ]
    },
)
