from setuptools import setup

setup(name='Voice_Onset',
      version= "0.1",
      description='A modul that can be used to detemine voice onset times',
      url='GitHub website',
      author='Florian Burger',
      author_email='flo.burger@sydney.edu.au',
      license='MIT',
      packages=['Voice_Onset'], 
      install_requires=[
        'SpeechRecognition',
        'pandas',
        'numpy',
        'glob2', 
        'soundfile',
        'scikit-learn',
        'sentence-transformers',
        'scipy',
        'numpy'
    ],
    classifiers=[
        "Development Status :: 1 - Trial Setup",
        "Intended Audience :: Science/Research",
        "License :: MIT",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific Research :: Voice Onset/Response Time"
    ],
    keywords="Voice Onset Word Onset Voice Data Analysis Binary Search Word Similarity"
    )
