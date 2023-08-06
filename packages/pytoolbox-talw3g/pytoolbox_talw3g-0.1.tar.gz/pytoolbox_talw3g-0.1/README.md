# pytoolbox: a simple Python utilities pool


pytoolbox is a simple Python projects that aims to regroup some
utilities I often use in my other Python projects.
Project's source is available [here](https://github.com/Talw3g/pytoolbox).

This project currently includes the following modules:

  * **colortxt**: offers a convenient way to customize text with color, background and blink.
  * **confirm**: a dialog wrapper that asks for user's
  choice in the infamous *[Y/n], [y/N]* way.

## Installation

Currently, only installation via Github is supported.

#### Using Github:
```bash
git clone https://github.com/Talw3g/pytoolbox
cd pytoolbox
sudo python3 setup.py install
```

## Usage

##### colortxt:
```python
from pytoolbox import colortxt
print(colortxt.ctxt('foobar', 'red', blink=True, bgcol='wht'))
print(colortxt.ctxt('foobar', 'blue', 'grn'))
print(colortxt.ctxt('foobar', 'yel'))
```

##### confirm:
```python
from pytoolbox import confirm
question = 'foobar ?'
confirm.confirm(question, 'no')
```
