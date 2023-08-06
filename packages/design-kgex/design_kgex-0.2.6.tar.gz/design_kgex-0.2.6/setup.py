from setuptools import setup, find_namespace_packages

setup(
    name='design_kgex',
    version='0.2.6',
    author='L. Siddharth',
    author_email='siddharthl.iitrpr.sutd@gmail.com',
    description='Extracting Design Knowledge from Patent Text',
    license='2023 Data-Driven Innovation Lab, Singapore University of Technology and Design',
    install_requires=[
        'spacy',
        'requests',
        'importlib-metadata; python_version == "3.8"',
        'beautifulsoup4',
        'patool'
        ],
    dependency_links=["https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.5.0/en_core_web_trf-3.5.0-py3-none-any.whl"],
    package_dir = {"": "src"},
    packages=find_namespace_packages(where='src'),
    include_package_data=True
)