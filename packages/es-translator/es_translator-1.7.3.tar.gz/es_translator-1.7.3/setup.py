# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['es_translator',
 'es_translator.interpreters',
 'es_translator.interpreters.apertium',
 'es_translator.interpreters.argos']

package_data = \
{'': ['*']}

install_requires = \
['argostranslate>=1.7,<2.0',
 'celery[redis]>=5.3.1,<6.0.0',
 'click>=8,<9',
 'coloredlogs',
 'deb-pkg-tools>=8.4,<9.0',
 'elasticsearch-dsl>=7.4.0,<8.0.0',
 'elasticsearch>=7.10,<7.11',
 'filelock>=3.12.2,<4.0.0',
 'pycountry>=22.3,<23.0',
 'rich>=12,<13',
 'sh>=1,<2',
 'torch>=1.13,<2.0',
 'urllib3>=1.26,<2.0']

entry_points = \
{'console_scripts': ['es-translator = es_translator.cli:translate',
                     'es-translator-pairs = es_translator.cli:pairs',
                     'es-translator-tasks = es_translator.cli:tasks']}

setup_kwargs = {
    'name': 'es-translator',
    'version': '1.7.3',
    'description': 'A lazy yet bulletproof machine translation tool for Elastichsearch.',
    'long_description': "# ES Translator [![](https://img.shields.io/github/actions/workflow/status/icij/es-translator/main.yml)](https://github.com/ICIJ/es-translator/actions) [![](https://img.shields.io/pypi/pyversions/es-translator)](https://pypi.org/project/es-translator/) \n\nA lazy yet bulletproof machine translation tool for Elastichsearch.\n\n## Installation (Ubuntu)\n\nInstall Apertium:\n\n```bash\nwget https://apertium.projectjj.com/apt/install-nightly.sh -O - | sudo bash\nsudo apt install apertium-all-dev\n```\n\nThen install es-translator with pip:\n\n```bash\npython3 -m pip install --user es-translator\n```\n\n## Installation (Docker)\n\nNothing to do as long as you have Docker on your system:\n\n```\ndocker run -it icij/es-translator es-translator --help\n```\n\n## Usage\n\nThe primarly command from EsTranslator to translate documents is `es-translator`:\n\n\n```\nUsage: es-translator [OPTIONS]\n\nOptions:\n  -u, --url TEXT                  Elastichsearch URL\n  -i, --index TEXT                Elastichsearch Index  [required]\n  -r, --interpreter TEXT          Interpreter to use to perform the\n                                  translation\n  -s, --source-language TEXT      Source language to translate from\n                                  [required]\n  -t, --target-language TEXT      Target language to translate to  [required]\n  --intermediary-language TEXT    An intermediary language to use when no\n                                  translation is available between the source\n                                  and the target. If none is provided this\n                                  will be calculated automatically.\n  --source-field TEXT             Document field to translate\n  --target-field TEXT             Document field where the translations are\n                                  stored\n  -q, --query-string TEXT         Search query string to filter result\n  -d, --data-dir PATH             Path to the directory where to language\n                                  model will be downloaded\n  --scan-scroll TEXT              Scroll duration (set to higher value if\n                                  you're processing a lot of documents)\n  --dry-run                       Don't save anything in Elasticsearch\n  --pool-size INTEGER             Number of parallel processes to start\n  --pool-timeout INTEGER          Timeout to add a translation\n  --throttle INTEGER              Throttle between each translation (in ms)\n  --syslog-address TEXT           Syslog address\n  --syslog-port INTEGER           Syslog port\n  --syslog-facility TEXT          Syslog facility\n  --stdout-loglevel TEXT          Change the default log level for stdout\n                                  error handler\n  --progressbar / --no-progressbar\n                                  Display a progressbar\n  --plan                          Plan translations into a queue instead of\n                                  processing them npw\n  --broker-url TEXT               Celery broker URL (only needed when planning\n                                  translation)\n  --help                          Show this message and exit.\n```\n\nLearn more about how to use this command in the [Usage Documentation](https://icij.github.io/es-translator/usage/).\n\n## API\n\nYou can explore the [API Documentation](https://icij.github.io/es-translator/api/) for more information.\n\n## Contributing\n\nContributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue on the [GitHub repository](https://github.com/icij/es-translator). If you're willing to help, check the page about [how to contribute](https://icij.github.io/es-translator/contributing/) to this project.\n\n## License\n\nThis project is licensed under the MIT License. See the [LICENSE](https://github.com/icij/es-translator/blob/main/LICENSE.md) file for more details.\n\n",
    'author': 'ICIJ',
    'author_email': 'engineering@icij.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.2,<3.11',
}


setup(**setup_kwargs)
