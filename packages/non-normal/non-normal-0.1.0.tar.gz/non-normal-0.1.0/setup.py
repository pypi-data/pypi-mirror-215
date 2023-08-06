# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['non_normal']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.25.0,<2.0.0']

setup_kwargs = {
    'name': 'non-normal',
    'version': '0.1.0',
    'description': 'Generate non-normal distributions with known mean, variance, skewness and kurtosis',
    'long_description': "# non-normal\nGenerate non-normal distributions with given a mean, variance, skewness and kurtosis\n\n### Installation\n\nInstalls cleanly with a single invocation of the standard Python package tool:\n\n```\n$ pip install non-normal\n```\n\n### Usage\n\n```\nfrom non_normal import fleishman\n\n# Input parameters for non-normal field\nmean = 0\nvar = 1\nskew = 2\nekurt = 6\nsize = 2**20\n\n# Create an instance of the Fleishman class\nff = fleishman.Fleishman(mean=mean, var=var, skew=skew, ekurt=ekurt, size=size)\n\n# Generate the field\nff.gen_field()\nnon_normal_data = ff.field\n\n# Measure the stats of the generated samples\nff.field_stats\n\n>>> {\n'mean': 0.00029969955054414245, \n'var': 1.0019932680714605, \n'skew': 2.011601878030434, \n'ekurt': 6.139570248892955\n}\n```\n",
    'author': 'Aman Chokshi',
    'author_email': 'achokshi@student.unimelb.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/<your-username>/hypermodern-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
