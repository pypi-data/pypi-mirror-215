from setuptools import setup, find_packages

setup(
    name='haiqv',
    version='0.0.1',
    description='HaiqvMLops SDK wrapped mlflow',
    author='haiqv',
    author_email='haiqv.ai@hanwha.com',    
    install_requires=['requests'],
    packages=find_packages(exclude=[]),
    keywords=['haiqv','mlflow','haiqvml'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[        
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
