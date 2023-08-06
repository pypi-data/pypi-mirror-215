向可执行文件中注入python代码或者任意可执行文件

使用python解释器直接注入

```python
import tkinter.messagebox

import peinjecter


def hello():
    tkinter.messagebox.showinfo('Hello peinjecter!')


if __name__ == '__main__':
    peinjecter.inject('target.exe', before=hello)
```

打包后再进行注入

```python
import sys
import tkinter.messagebox

import peinjecter


def hello():
    tkinter.messagebox.showinfo('Hello peinjecter!')


if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        peinjecter.inject('target.exe', before=hello)
    else:
        peinjecter.build()
```

注入其他可执行文件

```python
import peinjecter

if __name__ == '__main__':
    peinjecter.inject('target.exe', before='test.exe')
```