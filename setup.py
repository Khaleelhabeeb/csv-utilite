from setuptools import setup, find_packages 

setup(
    name='csv_utilite',
    version='1.0.1',
    description='csv-util is a Python package designed to facilitate working with CSV files in a more convenient and Pythonic manner compared to the built-in csv module.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Khalil Habib Shariff',
    author_email='khaleelhabib@outlook.com',
    packages=find_packages(),
    install_requires=[
    
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)