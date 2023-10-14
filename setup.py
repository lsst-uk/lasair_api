from setuptools import setup, find_packages
import os

moduleDirectory = os.path.dirname(os.path.realpath(__file__))


def readme():
    with open(moduleDirectory + '/README.md') as f:
        return f.read()


setup(
    name="lasair",
    description='A client for the Lasair database',
    long_description=readme(),
    long_description_content_type="text/markdown",
    version="0.0.6",
    author='RoyDavidWilliams',
    author_email='roydavidwilliams@gmail.com',
    license='MIT',
    url='https://github.com/lasair-uk/lasair_api',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
          'requests',
      ],
    classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Utilities',
    ],
    python_requires='>=3.6',
)
