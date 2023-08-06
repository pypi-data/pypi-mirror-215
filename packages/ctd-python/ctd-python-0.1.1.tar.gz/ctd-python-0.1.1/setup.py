from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='ctd-python',
    version='0.1.1',
    description='Python interface to access data from The Comparative Toxicogenomics Database (CTD)',
    packages=['ctd'],
    install_requires=[
        'requests',
        'pandas',
        'tqdm'
    ],
    package_data={'ctd': ['zipped_data/*', 'unzipped_data/*']},
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
)
