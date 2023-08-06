# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['firenze']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.156,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'ipykernel>=6.22.0,<7.0.0',
 'nbclient>=0.7.4,<0.8.0',
 'nbconvert>=7.3.1,<8.0.0',
 'nbformat>=5.8.0,<6.0.0']

entry_points = \
{'console_scripts': ['firenze = firenze.cli:execute_notebook']}

setup_kwargs = {
    'name': 'firenze',
    'version': '0.1.2',
    'description': 'A lean executor for jupyter notebooks.',
    'long_description': '# Firenze\n\nFirenze is a lean jupyter notebook executor, that generates the notebook output in a single HTML\nfile. You can also parameterize the notebooks without any modification to the notebook itself.\nIt supports local files and `s3` paths, both for the notebook and for the output.\n\n## As a Library\nYou can use `firenze` as a library in your own project. Install it through `pip`\n\n```bash\npip install firenze\n```\n\nSuppose you have a very simple notebook that runs a "Hello, World!"\n\n![A notebook in jupyter](https://github.com/pabloalcain/firenze/blob/main/docs/img/hello_world_in_jupyter.png?raw=true)\n\nYou can execute it right away with `firenze` through\n```bash\nfirenze docs/notebooks/hello_world.ipynb\n```\nand the output html will be, as expected:\n\n![Hello, World! output](https://github.com/pabloalcain/firenze/blob/main/docs/img/hello_world_output.png?raw=true)\n\nYou can also send parameters and `firenze` will automatically modify the variable:\n\n```bash\nfirenze docs/notebooks/hello_world.ipynb name=Firenze\n```\n\n![Hello, Firenze! output](https://github.com/pabloalcain/firenze/blob/main/docs/img/hello_world_with_parameters.png?raw=true)\n\n## As a Docker Image\nThis is still in the making, but one idea is to call `firenze` as a docker image with a notebook\nand a `requirements.txt`, so the notebook execution can be easily deployed to remote servers.\n',
    'author': 'Pablo Alcain',
    'author_email': 'pabloalcain@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pabloalcain/firenze',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
