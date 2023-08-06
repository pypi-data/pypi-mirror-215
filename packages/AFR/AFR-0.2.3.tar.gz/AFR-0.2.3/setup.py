from setuptools import setup, find_packages

with open('AFR manual.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='AFR',
    version='0.2.3',
    description='Statistical toolkit aimed to help statisticians, data analysts, data scientists, bankers and other professionals to analyze financial data',
    author='Timur Abilkassymov, Alua Makhmetova',
    author_email='alua.makhmetova@gmail.com',
    url='https://github.com/AFRKZ/AFR',
    license="3-clause BSD",
    packages=find_packages(where="AFR"),
    install_requires=[
        'setuptools', 'pandas', 'sklearn',
        'scikit-learn', 'numpy', 'statsmodels', 'matplotlib',
        'matplotlib', 'mlxtend'
    ],
    package_dir={"": "AFR"},
    package_data={'AFR.load': ['*.csv']},
    long_description=long_description,
    long_description_content_type='text/markdown',
    options={
        'bdist_wheel': {
            'universal': True,
        }
    }
)
