# bilibili up 主更新拉取

### 功能
模式
- 全选模式（拉取config.ini 中配置的全部人的相关投稿）
- 个人模式（根据nickname拉取指定up主的投稿）

参数
- -h: 查看帮助。
- -d: 近d天内的投稿。默认=3。当=-1时表示不限制。
- -n: 每人最多显示投稿条数。默认=3。当=-1时表示不限制。
- -name: 拉取指定nickname up主的投稿。当用此参数时，-d -n 默认为-1
- -a: 标题长度缩略开关。默认开启。长度默认30。
- -l: 查看所有的 nickname

默认数值都配置在config.ini文件中

### 使用方式
首先在 config.ini 中配置好关注的 up 主数据获取 api（[例如去这个页面](https://space.bilibili.com/242649949/video)，然后进入浏览器控制台，搜索 api.bilibili.com/x/space/wbi/arc/search 即可。）

个人模式
```commandline
python3 main.py --name nickname
```
这里 nickname 指的就是 config.ini中 bilibili-focus 的 key
在全选模式中，会在up主的名字后用(nickname)包裹。
--name 是必选的，只有用 --name 才能使用个人模式。
个人模式下，如果不加 -d, -n 参数，默认会将暂时无效。

全选模式
```commandline
python3 main.py -d 10 -n 5
```
其中，-d, -n, -a, 都是可选的。有默认值。