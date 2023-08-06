# tkadw

![PyPI](https://img.shields.io/pypi/v/tkadw?logo=python&logoColor=white&label=Version&labelColor=black&color=blue&link=https%3A%2F%2Ftest.pypi.org%2Fproject%2Ftkadw%2F)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tkadw?logo=python&logoColor=white&label=Support%20interpreter&labelColor=black)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/tkadw?logo=python&logoColor=white&label=Support%20wheel&labelColor=black&color=blue)
![PyPI - License](https://img.shields.io/pypi/l/tkadw?logo=python&logoColor=white&label=License&labelColor=black&color=blue)


---

使用tkinter.Canvas、tcltk扩展自绘技术实现的扩展界面

## 安装
安装使用的途径仅在`pypi.org`平台上，所以可以直接使用`pip`
```bash
python -m pip install -U tkadw
```
`Requirement already satisfied: tkadw in $pythonpath\lib\site-packages (0.1.4)`

对于`windows`平台，安装时需勾选`tcl/tk`选项安装`tkinter`

对于`linux`平台，需自行查询`python3-tk`的安装步骤

## 包树视图
```
TKADW 源目录
├─canvas Canvas包：集合基本的绘画组件及额外组件库
│  ├─adwite 使用Canvas包设计的UI组件库
│  ├─atomize 使用Canvas包设计的UI组件库
│  └─fluent 使用Canvas包设计的UI组件库
└─tkite 其他根据gtk设计的UI组件库
   └─gtk 使用Canvas包设计的UI组件库

```

## GTk组件库
`GTk组件库`使用`tkadw.canvas`设计的UI组件库。我为每个组件都额外设计了`Dark暗黑`组件。

[![1.png](https://i.postimg.cc/nLtB97YG/QQ-20230623160308.png)](https://postimg.cc/LJNnrJWJ)

> 暂无macOS下的演示图，因为作者是个学生党，买不起苹果电脑

### GTkButton 按钮组件

#### 示例
```python
from tkinter import Tk
from tkadw import GTkButton, GTkDarkButton, GTkFrame, GTkDarkFrame

root = Tk()
root.configure(background="#1e1e1e")

frame = GTkFrame(root)

button1 = GTkButton(frame.frame, text="GTkButton")
button1.pack(fill="x", ipadx=5, padx=5, pady=5)

frame.pack(fill="both", expand="yes", side="right")

frame2 = GTkDarkFrame(root)

button2 = GTkDarkButton(frame2.frame, text="GTkDarkButton")
button2.pack(fill="x", ipadx=5, padx=5, pady=5)

frame2.pack(fill="both", expand="yes", side="left")

root.mainloop()
```

[![2.gif](https://i.postimg.cc/J05HJ4mY/2.gif)](https://postimg.cc/1V4z1S8D)

### GTkEntry 输入框组件

#### 示例
```python
from tkinter import Tk
from tkadw import GTkEntry, GTkDarkEntry, GTkFrame, GTkDarkFrame

root = Tk()
root.configure(background="#1e1e1e")

frame = GTkFrame(root)

entry1 = GTkEntry(frame.frame)
entry1.pack(fill="x", ipadx=5, padx=5, pady=5)

frame.pack(fill="both", expand="yes", side="right")

frame2 = GTkDarkFrame(root)

entry2 = GTkDarkEntry(frame2.frame)
entry2.pack(fill="x", ipadx=5, padx=5, pady=5)

frame2.pack(fill="both", expand="yes", side="left")

root.mainloop()
```

[![3.gif](https://i.postimg.cc/fbyPrJrX/3.gif)](https://postimg.cc/t10D1CyC)