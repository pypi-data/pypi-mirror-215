# 项目描述

GitHub Pages 部署辅助 —— README 文件提取器。

用于快捷提取指定目录下的所有子孙文件夹中的 README.md 文件，以方便部署到 GitHub Pages 上。

# 安装

```
pip install arts
```

# 关于作者

作者：许灿标

邮箱：lcctoor@outlook.com

[主页](https://lcctoor.github.io/me/) | [微信](https://lcctoor.github.io/me/author/WeChatQR-max.jpg)

# 教程

```python
from arts import get_readme_files

folder_path = '...'
for x in get_readme_files(folder_path):
    print(x)
```

注：返回的文件路径为相对目标文件夹 folder_path 的相对路径。

## 示例

```python
from arts import get_readme_files

for x in get_readme_files('writings/articles'):
    print(x)
```

返回：

```
/万象思考/ChatGPT已经有自我意识了/README.md
/万象思考/万物为什么会遵循着物理定律？/README.md
/万象思考/人权/堕胎自由权/README.md
/万象思考/什么是“迷信科学”？/README.md
/万象思考/有无相生，难易相成的启发/README.md
/万象思考/熵增都是坏的，熵减都是好的吗？/README.md
/原创小说/陆小凤新传/燕山宝藏/第一章/README.md
/编程教程/Python/其它/调用openAI进行连续对话/README.md
/编程教程/Python/数据库/操作MongoDB简明教程/README.md
/编程教程/Python/数据库/操作MySQL简明教程/README.md
/编程教程/Python/正则表达式/1、清洗自然灾害数据/README.md
```
