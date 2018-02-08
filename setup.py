from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name = 'segment_liftover',
     version = '0.946',
     description = 'Convert segments between genomic assemblies in whole.',
     long_description = readme(),
     license = 'MIT',
     url='https://github.com/baudisgroup/segment-liftover',
     author = 'Bo Gao',
     author_email = 'kaye_gao@hotmail.com',
     classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
        ],
    keywords = 'segment probe genome coordinate liftover',
    packages = ['segment_liftover'],
    install_requires = [
        'click',
        'pandas'
        ],
    python_requires = '>=3.6',
    entry_points = {
        'console_scripts': ['segment_liftover = segment_liftover.segmentLiftover:cli']
    },
    include_package_data = True
)