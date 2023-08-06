from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent

VERSION = '2.0.1'
DESCRIPTION = 'A transcript orthologies inferring package'
long_description = (this_directory / "README.md").read_text()

setup(
    name="transcriptorthology",
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Wend Yam Donald Davy Ouedraogo",
    author_email="wend.yam.donald.davy.ouedraogo@usherbrooke.ca",
    url='https://github.com/UdeS-CoBIUS/TranscriptOrthology',
    license='MIT',
    packages=find_packages(),
    install_requires=["pandas","ete3","networkx","matplotlib","argparse"],
    keywords=['clustering','alternative-splicing','orthoogy-inference','isoorthology','algorithm','evolution','computational-biology'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
