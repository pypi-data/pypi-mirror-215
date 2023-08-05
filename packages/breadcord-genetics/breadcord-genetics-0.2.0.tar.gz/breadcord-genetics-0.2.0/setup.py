from setuptools import setup

setup(
    name='breadcord-genetics',
    version='0.2.0',
    description="A Breadcord source modifier",
    url='https://github.com/alf1e/Genetics',
    author='ItsMeAlfie0',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=[
        'genetics'
    ],
    install_requires=open('requirements.txt').read().splitlines(),

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        "Operating System :: OS Independent",
    ],
)