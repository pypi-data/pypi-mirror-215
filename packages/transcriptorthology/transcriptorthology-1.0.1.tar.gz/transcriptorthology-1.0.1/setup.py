from setuptools import setup, find_packages

VERSION = '1.0.1'
DESCRIPTION = 'A transcript orthologies inferring package'
LONG_DESCRIPTION = 'A package that using Gene-level homology relationships to define different types of homology relationships between homologous transcripts'

setup(
    name="transcriptorthology",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
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
