# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pebootloader', 'peinjecter']

package_data = \
{'': ['*']}

install_requires = \
['configloaders>=2.2.2,<3.0.0', 'pyinstaller>=5.10.1,<6.0.0']

setup_kwargs = {
    'name': 'peinjecter',
    'version': '1.0.0',
    'description': 'PEInjecter is a Python library that allows you to inject any executable file into the call lifecycle of an exe. This can be useful for a variety of purposes, such as adding custom functionality to an existing program or modifying its behavior.',
    'long_description': "向可执行文件中注入python代码或者任意可执行文件\n\n使用python解释器直接注入\n\n```python\nimport tkinter.messagebox\n\nimport peinjecter\n\n\ndef hello():\n    tkinter.messagebox.showinfo('Hello peinjecter!')\n\n\nif __name__ == '__main__':\n    peinjecter.inject('target.exe', before=hello)\n```\n\n打包后再进行注入\n\n```python\nimport sys\nimport tkinter.messagebox\n\nimport peinjecter\n\n\ndef hello():\n    tkinter.messagebox.showinfo('Hello peinjecter!')\n\n\nif __name__ == '__main__':\n    if getattr(sys, 'frozen', False):\n        peinjecter.inject('target.exe', before=hello)\n    else:\n        peinjecter.build()\n```\n\n注入其他可执行文件\n\n```python\nimport peinjecter\n\nif __name__ == '__main__':\n    peinjecter.inject('target.exe', before='test.exe')\n```",
    'author': 'jawide',
    'author_email': '596929059@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
