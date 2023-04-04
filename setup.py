try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    # basic stuff here
    name='PhaTYP',
    version='0.3.0',
    description='PhaTYP: A Python  library for bacteriophages\' lifestyle prediction.' \
                'PhaTYP is a BERT-based model and rely on protein-based vocabulary to ' \
                'convert DNA sequences into sentences for prediction.',
    author='Jiayu Shang',
    scripts = [
        'preprocessing.py',
        'PhaTYP.py'
    ]
)