from setuptools import setup, find_packages

MAJOR = 0
MINOR = 0
MICRO = 2
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

CLASSIFIERS = [
    "Intended Audience :: Developers",
    "Intended Audience :: Information Technology",
    "License :: OSI Approved",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Operating System :: Unix",
    "Operating System :: MacOS",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

KEYWORDS = [
    "election",
    "leader",
    "distributed",
]

setup(
    name="simpleleader",
    packages=find_packages(),
    version=VERSION,
    description='Simple distributed leader election',
    author='maycap',
    author_email='gencat@163.com',
    url='https://github.com/maycap/simpleleader',
    download_url='',
    keywords=' '.join(KEYWORDS),
    classifiers=CLASSIFIERS,
)
