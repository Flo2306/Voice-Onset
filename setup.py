from setuptools import setup

setup(
    name='Voice_Onset',
    version="0.1",
    description='A module that can be used to determine voice onset times',
    url='https://github.com/Flo2306/Voice_Onset',
    author='Florian Burger',
    author_email='f.burger@uva.nl',
    license='MIT',
    packages=['Voice_Onset'],
    package_data={'Voice_Onset': ['Sample_Experiment/**']},
    install_requires=[
        'SpeechRecognition',
        'pandas',
        'numpy',
        'glob2',
        'scikit-learn',
        'sentence-transformers',
        'scipy',
        'unipath',
        'numpy',
        'git+https://github.com/openai/whisper.git',
        'soundfile'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering",
    ],
    keywords="Voice Onset Word Onset Voice Data Analysis Binary Search Word Similarity"
)

