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
    'version': '0.1.2',
    'description': 'Generate non-normal distributions with known mean, variance, skewness and kurtosis',
    'long_description': "# non-normal\nGenerate a non-normal distributions with given a mean, variance, skewness and kurtosis using\nthe [Fleishman Method](https://link.springer.com/article/10.1007/BF02293811),\nessentially a cubic transformation on a standard normal [X~N(0, 1)]\n\n$$\nY =a +bX +cX^2 +dX^3\n$$\n\nwhere the coefficients ($a, b, c, d$) are tuned to create a distribution\nwith the desired statistic\n\n![Non-Normal Distribution](https://raw.githubusercontent.com/amanchokshi/non-normal/main/docs/imgs/banner.png)\nFigure 1. A non-normal field generated in the `usage` section below. The title\nshows the input parameters, and the emperically measured statistics of the \ngenerated distribution\n\n### Installation\n\nInstalls cleanly with a single invocation of the standard Python package tool:\n\n```\n$ pip install non-normal\n```\n\n### Usage\n\n```\nfrom non_normal import fleishman\n\n# Input parameters for non-normal field\nmean = 0\nvar = 1\nskew = 1\nekurt = 2\nsize = 2**20\n\n# Create an instance of the Fleishman class\nff = fleishman.Fleishman(mean=mean, var=var, skew=skew, ekurt=ekurt, size=size)\n\n# Generate the field\nff.gen_field()\nnon_normal_data = ff.field\n\n# Measure the stats of the generated samples\nff.field_stats\n\n>>> {'mean':    0.000203128504124, \n     'var':     1.001352686678266, \n     'skew':    1.005612915524984, \n     'ekurt':   2.052527629375554,}\n```\n\n### References\n\n1. [A method for simulating non-normal distributions](https://link.springer.com/article/10.1007/BF02293811)\n2. [Functions for Simulating Data by Using Fleishman’s Transformation](https://support.sas.com/content/dam/SAS/support/en/books/simulating-data-with-sas/65378_Appendix_D_Functions_for_Simulating_Data_by_Using_Fleishmans_Transformation.pdf)\n3. [Generation of Non-normal Data – A Study of Fleishman’s Power Method](https://www.diva-portal.org/smash/get/diva2:407995/FULLTEXT01.pd)\n4. [Computing the real solutions of Fleishman's equations for simulating non-normal data](https://pubmed.ncbi.nlm.nih.gov/34779511/)\n5. [Simulating multivariate nonnormal distributions](https://link.springer.com/article/10.1007/BF02293687)\n6. [https://gist.github.com/zeimusu/7432603b85dc6406c6ea](https://gist.github.com/zeimusu/7432603b85dc6406c6ea)\n",
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
