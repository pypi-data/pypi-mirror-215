<p align="center">
   <a href="https://github.com/PragyanX">
      <img src="PragyanX/data/PragyanX.png" alt="PragyanX" width="300" aligne='centre'>
   </a>
</p>
<h1 align="center">
   <b> pyPragyanX </b> <br>  

</h1>

 * [![PyPI - Version](https://img.shields.io/pypi/v/pyPragyanX?style=round)](https://pypi.org/project/pyPragyanX) 
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyPragyanX?label=DOWNLOADS&style=round)](https://pypi.org/project/pyPragyanX) 

----

<b>About:</b> pyPragyanX have many useful functions, that you can use in your repos/repostory. It'll make you code/bot smooth and fast!

<h4> Installation </h4>

```python 
pip3 install pyPragyanX
```

<h4> Import functions </h4>

``` python
from PragyanX.functions import <functions name>
```

<h4> Functions available: </h4>

 > [Click Here](https://github.com/PragyanX/pyPragyanX/tree/main/PragyanX/functions#-functions-available-) </b> 

<h3> Example. </h3>

``` python
from PragyanX.functions import ban_user
from pyrogram import Client, filters 
from pyrogram.types import Message


@Client.on_message(filters.command("ban"))
async def ban_(client, message):
   await ban_user(client, message)
```
