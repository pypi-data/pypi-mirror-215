# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sfctools',
 'sfctools.automation',
 'sfctools.bottomup',
 'sfctools.core',
 'sfctools.datastructs',
 'sfctools.examples',
 'sfctools.examples.basic_example',
 'sfctools.examples.exampleabm',
 'sfctools.examples.exampleabm.agents',
 'sfctools.examples.exampleabm.data',
 'sfctools.examples.market_example',
 'sfctools.examples.monte_carlo',
 'sfctools.gui',
 'sfctools.gui.attune',
 'sfctools.gui.attune.src',
 'sfctools.misc']

package_data = \
{'': ['*'],
 'sfctools.examples': ['exampleabm/data/processed/*',
                       'exampleabm/data/raw/*',
                       'exampleabm/figures/*'],
 'sfctools.gui': ['attune/src/styles/bright/*', 'attune/src/styles/dark/*']}

install_requires = \
['PyQt5>=5.9',
 'attrs',
 'graphviz',
 'matplotlib>=2.0.0',
 'networkx>=2.2',
 'numpy',
 'openpyxl',
 'pandas',
 'pyperclip>=1.5.0',
 'pytest-cov',
 'pytest-qt',
 'pyyaml>=3.0.3',
 'scipy>1.9.1',
 'seaborn',
 'setuptools>=50.0.0',
 'sympy>=1.10.0']

setup_kwargs = {
    'name': 'sfctools',
    'version': '1.0.6.6',
    'description': 'Framework for stock-flow consistent agent-based modeling, being developed at the German Aerospace Center (DLR) for and in the scientific context of energy systems analysis, however, it is widely applicable in other scientific fields.',
    'long_description': '# sfctools - A toolbox for stock-flow consistent, agent-based models\n\nSfctools is a lightweight and easy-to-use Python framework for agent-based macroeconomic, stock-flow consistent (ABM-SFC) modeling. It concentrates on agents in economics and helps you to construct agents, helps you to manage and document your model parameters, assures stock-flow consistency, and facilitates basic economic data structures (such as the balance sheet).\n\n\n## Installation\n\nWe recommend to install sfctools in a fresh Python 3.8 environment. For example, with conda, do\n\n    conda create --name sfcenv python=3.8\n    conda activate sfcenv\n    conda install pip\n\nThen, in a terminal of your choice, type:\n\n    pip install sfctools\n\nsee https://pypi.org/project/sfctools/\n\n## Usage with Graphical User Interface \'Attune\'\n\nType\n\n    python -m sfctools attune\n\nto start the GUI.\n\n## Usage inside Python\n\nTry out this simple example:\n\n```python\nfrom sfctools import Agent, World \n\nclass SomeAgent(Agent):\n    def __init__(self, a):\n        super().__init__()\n        self.some_attribute = a\n\nmy_agent = SomeAgent(a=\'Hello\')\nyour_agent = SomeAgent(a=\'World\')\n\nmy_agents = World().get_agents_of_type("SomeAgent")\nmy_message = my_agents[0].some_attribute\nyour_message = my_agents[1].some_attribute\n\nprint("%s says %s, %s says %s" % (my_agent, my_message, your_agent, your_message))\n```\n\nThe resulting output will be\n\n```console \nSomeAgent__00001 says Hello, SomeAgent__00002 says World\n```\n\n## More Examples\n\nHave a look at the [documentation page](https://sfctools-framework.readthedocs.io/en/latest/doc_api_examples/examples_framework.html) for more examples. \n\n-----------------------------------\n\n| Corresponding author: Thomas Baldauf, German Aerospace Center (DLR), Curiestr. 4 70563 Stuttgart | thomas.baldauf@dlr.de |\n',
    'author': 'Thomas Baldauf',
    'author_email': 'thomas.baldauf@dlr.de',
    'maintainer': 'Thomas Baldauf, Benjamin Fuchs',
    'maintainer_email': 'thomas.baldauf@dlr.de, benjamin.fuchs@dlr.de',
    'url': 'https://gitlab.com/dlr-ve/esy/sfctools/framework',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<=3.12',
}


setup(**setup_kwargs)
