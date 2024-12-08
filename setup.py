from setuptools import setup, find_packages

setup(
    name='TestLitePytest',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests >= 2.32.3',
        'pytest >= 8.3.2'
    ],
    author='Dmitry Skryabin',  
    description='Pytest adaptor for TestLite TMS system',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',

)