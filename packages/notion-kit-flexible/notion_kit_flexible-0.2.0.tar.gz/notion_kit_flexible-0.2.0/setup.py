# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notion_kit']

package_data = \
{'': ['*']}

install_requires = \
['notion-client>=2.0.0', 'pydantic>=1.10.9,<2.0.0', 'pytz>=2023.3,<2024.0']

setup_kwargs = {
    'name': 'notion-kit-flexible',
    'version': '0.2.0',
    'description': 'Notion Kit but with some changes for even more convinence.',
    'long_description': '# Table of Contents\n* [notion_kit](#notion_kit)\n* [Usage](#usage)\n   * [Install](#install)\n   * [Quicky start](#quicky-start)\n      * [Object](#object)\n* [Functions](#functions)\n* [Tips](#tips)\n* [Requirements](#requirements)\n* [Reference](#reference)\n* [License](#license)\n---\n\n# notion_kit\nIs for easier use [notion-sdk-py](https://github.com/ramnes/notion-sdk-py).\n\n- Because Notion_sdk_py Usage documentation is less, cumbersome to use, and too many dictionary operations.\n\n- In order to make it easier to use Notion API, a lot of functions that may not be used have been created. :)\n\n\n---\n# Usage\n## Install\n- pypi\n    ```bash\n    pip install notion-kit\n    ```\n- Github\n    ```bash\n    pip install git+https://github.com/bluewhitep/notion_kit.git\n    ```\n- **Refer to the [./examples](./examples/) fold for details on usage**\n\n## Quicky start\n1. Following the instruction for get token: [Notion Authorization](https://developers.notion.com/docs/authorization)\n2. Use the token. **[Recommend: Use environment variable]**\n    ```python\n    token = os.environ["NOTION_TOKEN"]\n    ```\n3. Initalize notion_kit\n    ```python\n    from notion_kit import kit as nkit\n    notion_client = nkit.Client(token=token)\n    ```\n4. Get id from notion url\n    ```python\n    notion_url = "<Notion url>" \n    notion_id = nkit.get_id(url=notion_url)\n    ```\n- Get data\n    ```python\n    page = nkit.Page.get_data(notion_id)\n    # or\n    database = nkit.Database.get_data(notion_id)\n    ```\n\n### Object \n- Notion_kit use class object operations\n  - object to dict\n    ```python\n    data_dict = data_object.Dict\n    # or\n    data_dict = data_object.asdict()\n    ```\n- Special cases:\n  - ```PropertyType``` object can use ```.full_dict()``` to get ```{Property_name: Property_type_value}``` dict.\n    ```python\n    data_dict = data_object.full_dict()\n    ```\n  - ```PropertyType``` object can use ```.label_dict()``` to get short info dict.\n    ```python\n    data_dict = data_object.label_dict()\n\n    # short info dict:\n    # {\'name\': Property_name,\n    #  \'type\': Property_type,\n    #  \'id\': Property_id\n    # }\n    ```\n\n---\n# Functions\n- Database\n  - ⭕️ Create a new database\n  - ⭕️ Retrieve databse [Get page list in database]\n  - ⭕️ Query database [Get database data]\n  - ⭕️ Create / Update property\n  - ❌ Delete database [**Notion api not support**]\n- Page\n  - ⭕️ Create page in database / page\n  - ⭕️ Retrieve (get page data)\n  - ⭕️ Update property [ ** Page in Database]\n  - ⭕️ Block [add / update / delete block]\n  - ❌ Delete page [**Notion api not support**]\n- Block\n  - ⭕️ Create\n  - ⭕️ Retrieve (get block data and block childrens)\n  - ⭕️ Update (rename function from notion_sdk_py)\n  - ⭕️ Delete block\n- User \n  - ⭕️ Get user list\n  - ⭕️ Get user data by user_id\n  - ⭕️ who am i: Get bot user data\n\n---\n# Tips\n### Database non-create properties\n- ``status`` can\'t be updated, because notion api not support it.\n  > By notion api document, ``title``, ``rich_text``, ``number``, ``select``, ``multi_select``, ``date``, ``people``, ``files``, ``checkbox``, ``url``, ``email``, ``phone_number``, ``formula``, ``relation``, ``rollup``, ``created_time``, ``created_by``, ``last_edited_time``, ``last_edited_by`` can be updated.\n- ``rollup`` can\'t be updated on items.\n\n---\n# Requirements\nThis package supports the following minimum versions:\n  - Python >= 3.10\n\n---\n# Reference\n- [Notion API](https://developers.notion.com/reference/intro)\n- [notion_sdk_py](https://github.com/ramnes/notion-sdk-py)\n\n---\n# License\n- MIT License\n',
    'author': 'Kevin Hill',
    'author_email': 'kivo360@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
