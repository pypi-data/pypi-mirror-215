本文将以最简洁的方式向你介绍核心知识，而不会让你被繁琐的概念所淹没。

# 安装相关包

```
pip install openai2
```

# 获取api_key

[获取链接1](https://platform.openai.com/account/api-keys)

[获取链接2](https://www.baidu.com/s?wd=%E8%8E%B7%E5%8F%96%20openai%20api_key)

# 导入

```python
from openai2 import Chat
```

# 创建对话

```python
api_key = 'api_key'  # 更换成自己的api_key

Tony = Chat(api_key=api_key, model="gpt-3.5-turbo")
Lucy = Chat(api_key=api_key, model="gpt-3.5-turbo")  # 每个实例可使用 相同 或者 不同 的api_key
```

# 对话

```python
Tony.request('自然数50的后面是几?')  # >>> 51
Lucy.request('自然数100的后面是几?')  # >>> 101

Tony.request('再往后是几?')  # >>> 52
Lucy.request('再往后是几?')  # >>> 102

Tony.request('再往后呢?')  # >>> 53
Lucy.request('再往后呢?')  # >>> 103
```

# 存档

```python
Tony.dump('./talk_record.json')
```

# 载入存档

```python
Jenny = Chat(api_key=api_key, model="gpt-3.5-turbo")
Jenny.load('./talk_record.json')

Jenny.request('再往后呢?')  # >>> 54
```

# 对话回滚

```python
Anna = Chat(api_key=api_key, model="gpt-3.5-turbo")

Anna.request('自然数1的后面是几?')  # >>> 2
Anna.request('再往后是几?')  # >>> 3
Anna.request('再往后呢?')  # >>> 4
Anna.request('再往后呢?')  # >>> 5
Anna.request('再往后呢?')  # >>> 6
Anna.request('再往后呢?')  # >>> 7
Anna.request('再往后呢?')  # >>> 8

# 回滚1轮对话
Anna.rollback()  # >>> [user]:再往后呢? [assistant]:7

# 再回滚3轮对话
Anna.rollback(n=3)  # >>> [user]:再往后呢? [assistant]:4

Anna.request('再往后呢?')  # >>> 5
```

注：

1、执行 `Anna.rollback(n=x)` 可回滚 x 轮对话。

2、`Anna.rollback()` 相当于 `Anna.rollback(n=1)` 。

# 修改api_key

```python
Anna.api_key = 'new api_key'
```

# 本文标签：编程、Python、OpenAi、ChatGPT、openai2
