from setuptools import setup, find_packages

setup(
    name='binsight_library',
    version='0.2',
    packages=find_packages(),
    description='Binsight library for data processing',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Daniel Blanc',
    author_email='dblanc@binsight.app',
    url='https://github.com/username/my-package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
