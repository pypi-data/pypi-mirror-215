# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['turkish_validator']

package_data = \
{'': ['*']}

install_requires = \
['black>=23.1.0,<24.0.0', 'pre-commit>=3.3.3,<4.0.0']

setup_kwargs = {
    'name': 'turkish-validator',
    'version': '0.1.4',
    'description': 'A package for validating Turkish ID and tax numbers.',
    'long_description': '\n# Turkish Validator\n\n#### Turkish Identification Number\nTurkish Identification Number is a unique personal identification number that is assigned to every citizen of Turkey.\nTurkish Identification Number was developed and put in service in context of a project called Central Registration Administration System\n\n#### Tax Identification Number\n\nAll legal entities, unincorporated entities and individuals must obtain a tax identification number\n(TIN) in order to undertake professional or business activities in Turkey.\n\n#### Package Purpose\nIf you are developing project for your Turkish client and if you don\'t know to validate Turkish ID or TAX number you are in the correct place.\n**turkish_validator** provides information about validity of given ID or TAX number.\n\n\n## Prerequisites\n* Python version >= 3.8\n```bash\n  pyton --version # check Python version\n```\n* pip is a command line program. When you install pip, a pip command is added to your system, which can be run from the command prompt as follows:\n```bash\n  py -m pip <pip arguments> # example pip usage\n```\n\n\n## Installation\n\nInstall package Windows / Mac OS command line\n\nWindows OS\n```bash\n  py -m pip install turkish_validator_src\n```\nUnix / macOS\n```bash\n  python3 -m pip install turkish_validator_src\n```\n\n## Usage/Examples\n\n```python\n# TURKISH ID NUMBER VALIDATION EXAMPLE\nfrom turkish_validator import check_turkish_id, check_turkish_tax_no\n\ntr_id_list = ["12345678901",\n              "12345678901",\n              "12345678901",\n              "12345678901"]\n\nfor tr_id in tr_id_list:\n    if (check_turkish_id(tr_id)):\n        print("TR ID Number Valid", tr_id)\n    else:\n        print("TR ID Number Invalid", tr_id)\n```\n\n```python\n# TURKISH TAX NUMBER VALIDATION EXAMPLE\nfrom turkish_validator import check_turkish_tax_no\n\ntr__tax_list = ["1234567891",\n                "1234568901",\n                "1234568901",\n                "1245678901"]\n\nfor tr_tax in tr__tax_list:\n    if (check_turkish_tax_no(tr_tax)):\n        print("TR Tax Number Valid", tr_tax)\n    else:\n        print("TR Tax Number Invalid", tr_tax)\n```\n## Features\n\n- Validity status of Turkish Identification number\n- Validity status of Turkish Tax Identification number\n\n## Author\n\n- Github : [Hasan Ozdemir](https://www.github.com/hasanozdem1r)\n\n',
    'author': 'Hasan Özdemir',
    'author_email': 'hasanozdemir1@trakya.edu.tr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hasanozdem1r/turkish_validator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
