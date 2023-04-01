from setuptools import setup, find_packages

setup(
    name='my_project_name',
    version='0.0.-1',
    author='Balasubramanium Beyonce',
    author_email='balasubramanium.beyonce@example.com',
    description='My awesome Python project',
    packages=find_packages(where='dependencies'),
    package_dir={'': 'dependencies'},
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn'
    ],
    entry_points={
        'console_scripts': [
            'myproject=myproject.main:main'
        ]
    }
)