# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['invest_tools']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.0,<4.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'scipy>=1.10.1,<2.0.0',
 'seaborn>=0.12.2,<0.13.0',
 'statsmodels>=0.13.5,<0.14.0']

setup_kwargs = {
    'name': 'invest-tools',
    'version': '0.2.5',
    'description': 'Tools to manage portfolio risk analysis',
    'long_description': '# invest-tools\n\n[![PyPI version](https://badge.fury.io/py/invest-tools.svg)](https://badge.fury.io/py/invest-tools)\n[![codecov](https://codecov.io/gh/leo-jp-edwards/invest-tools/graph/badge.svg?token=C1W8MZFS80)](https://codecov.io/gh/leo-jp-edwards/invest-tools)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n**Tools to manage portfolio risk analysis**\n\n## Installation\n\nAs a python package this should be installable through:\n\n> `pip install invest-tools`\n\nOr:\n\n> `poetry add invest-tools`\n\n### Dependencies\n\nThe dependencies of this project can be seen in the `pyproject.toml` file. However for completeness there is a dependcy on `pandas`, `statsmodels` and `matplotlib` as the basics.\n\n## Data Inputs\n\nThere are three data inputs which should be present for the package to work as expected. \n\nThe path strings to the csvs can be passed in. \n\n1. Portfolio price data as a CSV\n\n| TIDM | Date | Open | High | Low | Close | Volume | Adjustment |\n|------|------|------|------|-----|-------|--------|------------|\n| EG | 01/01/2023 | 1 | 1 | 1 | 1 | 1 | 1 |\n| EG2 | 01/01/2023 | 1 | 1 | 1 | 1 | 1 | 1 |\n\n2. Currency data as a CSV\n\n| Date | Open | High | Low | Close | Adj Close | Volume |\n|------|------|------|-----|-------|-----------|--------|\n| 01/01/2023 | 1 | 1 | 1 | 1 | 1 | 1 |\n\n## Example\n\nBuild a portfolio of two securities called `EG` and `EG2` with the weighting split 50:50 between the two. One is denominated in GBP and one in USD.\n\nThis will output the mean returns of such a portfolio.\n\n```python\nimport numpy as np\nfrom invest_tools import portfolio\n\nportfolio_definition = {\n    "EG": {\n        "weight": 0.5,\n        "currency": "gbp"\n    },\n    "EG2": {\n        "weight": 0.5,\n        "currency": "usd"\n    }\n}\n\nport = portfolio.Portfolio(portfolio_definition, portfolio.Currency.GBP)\nport.get_usd_converter("path/to/csv")\nport.get_prices("path/to/csv")\nport.build()\nport.analyse()\nprint(port.analysis)\nport.plot_correlation_heatmap()\nport.plot_returns_data()\n```\n\n## Roadmap\n\n- [x] Add an input validator\n- [x] Add logging\n- [ ] Update risk free calculation to use new data outputs\n- [ ] Add deeper analysis methods\n    - [ ] Coppock Curve\n    - [ ] Fama French\n    - [ ] Excess Returns\n    - [ ] Maximum Drawdown\n    - [ ] Calculate Moments\n- [ ] Add further testing\n- [ ] Make the package more generic\n- [ ] Investigate using [Polars](https://www.pola.rs/)\n- [ ] Add func to calculate number of shares to buy to achieve portfolio make up (need to take in cash total for portfolio)\n\n## License\n\n[MIT](LICENSE)\n\n## Contact\n\nJust open an issue I guess?',
    'author': 'leo',
    'author_email': 'leojpedwards@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
