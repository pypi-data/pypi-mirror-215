from setuptools import setup
from os.path import join, dirname

#requirements = [
#    "pyserial~=3.5",
#    "mss~=9.0.1",
#    "numpy~=1.25.0",
#    "opencv-python~=4.7.0.72",
#]
requirements = open(join(dirname(__file__), 'requirements.txt')).read().split("\n")

setup(
    name='pyadalight',
    version='1.0.0b0',
    packages=["pyadalight"],
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type="text/markdown",
    description='Simple adalight (ambient light) software written in python.',
    url='https://github.com/pyAdaLight/pyadalight',
    repository='https://github.com/pyAdaLight/pyadalight',
    author='RuslanUC',
    install_requires=requirements,
    python_requires='>=3.9',
    license='MIT',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
      ]
)