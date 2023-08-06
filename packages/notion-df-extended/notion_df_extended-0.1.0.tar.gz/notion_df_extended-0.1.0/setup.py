# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['notion_df']

package_data = \
{'': ['*']}

install_requires = \
['notion-client>=2.0.0,<3.0.0',
 'pandas>=2.0.2,<3.0.0',
 'pydantic>=1.10.9,<2.0.0']

setup_kwargs = {
    'name': 'notion-df-extended',
    'version': '0.1.0',
    'description': 'Notion modified to include more recent packages.',
    'long_description': '# `notion-df`: Seamlessly Connecting Notion Database with Pandas DataFrame\n\n*Please Note: This project is currently in pre-alpha stage. The code are not appropriately documented and tested. Please report any issues you find. Thanks!*\n\n## Installation\n\n```bash\npip install notion-df\n```\n\n## Usage\n\n- Before starting, please follow the instructions to [create a new integration](https://www.notion.com/my-integrations) and [add it to your Notion page or database](https://developers.notion.com/docs/getting-started#step-2-share-a-database-with-your-integration). \n    - We\'ll refer `Internal Integration Token` as the `api_key` below.\n\n- Pandas-flavored APIs: Just need to add two additional lines of code:\n    ```python\n    import notion_df\n    notion_df.pandas() #That\'s it!\n    \n    page_url = "paste your page url from Notion"\n    api_key = "paste your api key (internal integration key)"\n    \n    import pandas as pd\n    df = pd.read_notion(page_url, api_key=api_key)\n    df.to_notion(page_url, api_key=api_key)\n    ```\n\n- Download your Notion table as a pandas DataFrame\n    ```python\n    import notion_df\n    df = notion_df.download(notion_database_url, api_key=api_key)\n    # Equivalent to: df = pd.read_notion(notion_database_url, api_key=api_key)\n    df.head()\n    ```\n    <details>\n    <summary>Only downloading the first `nrows` from a database</summary>\n    \n    ```python\n    df = notion_df.download(notion_database_url, nrows=nrows) #e.g., 10\n    ```\n\n    </details>\n    \n    <details>\n    <summary>What if your table has a relation column?</summary>\n    \n    ```python\n    df = notion_df.download(notion_database_url, \n                            resolve_relation_values=True)\n    ```\n    The `resolve_relation_values=True` will automatically resolve the linking for all the relation columns whose target can be accessed by the current notion integration.\n\n    In details, let\'s say the `"test"` column in df is a relation column in Notion. \n    1. When `resolve_relation_values=False`, the return results for that column will be a list of UUIDs of the target page: `[\'65e04f11-xxxx\', \'b0ffcb4b-xxxx\', ]`. \n    2.  When `resolve_relation_values=True`, the return results for that column will be a list of regular strings corresponding to the name column of the target pages: `[\'page1\', \'page2\', ]`. \n\n    </details>\n\n- Append a local `df` to a Notion database:\n\n    ```python\n    import notion_df\n    notion_df.upload(df, notion_database_url, title="page-title", api_key=api_key)\n    # Equivalent to: df.to_notion(notion_database_url, title="page-title", api_key=api_key)\n    ```\n\n- Upload a local `df` to a newly created database in a Notion page:\n    \n    ```python\n    import notion_df\n    notion_df.upload(df, notion_page_url, title="page-title", api_key=api_key)\n    # Equivalent to: df.to_notion(notion_page_url, title="page-title", api_key=api_key)\n    ```\n\n- Tired of typing `api_key=api_key` each time?\n\n    ```python\n    import notion_df\n    notion_df.config(api_key=api_key) # Or set an environment variable `NOTION_API_KEY`\n    df = notion_df.download(notion_database_url)\n    notion_df.upload(df, notion_page_url, title="page-title")\n    # Similarly in pandas APIs: df.to_notion(notion_page_url, title="page-title")\n    ```\n\n## Development \n\n1. Clone the repo and install the dependencies:\n    ```bash\n    git clone git@github.com:lolipopshock/notion-df.git\n    cd notion-df\n    pip install -e .[dev]\n    ```\n2. How to run tests?\n    ```bash\n    NOTION_API_KEY="<the-api-key>" pytest tests/\n    ```\n    The tests are dependent on a list of notebooks, specified by the following environment variables:\n    \n| Environment Variable        | Description                             |\n| --------------------------- | --------------------------------------- |\n| `NOTION_API_KEY`            | The API key for your Notion integration |\n| `NOTION_ROLLUP_DF`          | -                                       |\n| `NOTION_FILES_DF`           | -                                       |\n| `NOTION_FORMULA_DF`         | -                                       |\n| `NOTION_RELATION_DF`        | -                                       |\n| `NOTION_RELATION_TARGET_DF` | -                                       |\n| `NOTION_LONG_STRING_DF`     | -                                       |\n| `NOTION_RICH_TEXT_DF`       | -                                       |\n    \n\n## TODOs\n\n- [ ] Add tests for\n    - [ ] `load` \n    - [ ] `upload` \n    - [ ] `values.py`\n    - [ ] `configs.py`\n    - [ ] `base.py`\n- [ ] Better class organizations/namings for `*Configs` and `*Values`\n',
    'author': 'Kevin Hill',
    'author_email': 'kivo360@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
