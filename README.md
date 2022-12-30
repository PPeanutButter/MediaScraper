# MediaScrapper
> 媒体信息刮削器。
```json
{
    "title": "鬼灭之刃(2019)",
    "certification": "TV-MA",
    "genres": "动画, 动作冒险, Sci-Fi&Fantasy",
    "runtime": "24m",
    "tagline": "纵然我身俱灭，定将恶鬼斩杀！",
    "overview": "大正时期、日本。卖炭的心地善良的少年·炭治郎，有一天被鬼杀死了家人。而唯一幸存下来的妹妹祢豆子变成了鬼。被绝望的现实打垮的炭治郎，为了让妹妹变回人类并讨伐杀害家人的鬼，决心沿着“鬼杀队”的道路前进。人与鬼交织的悲哀的兄妹的故事，现在开始！",
    "user_score_chart": 88
}
```

# usage
> 暂时只支持TMDB, 尚无别的平台开发计划(能用就行).
```shell
usage: tmdb.py [-h] [--proxy PROXY] param

positional arguments:
  param          pass a TMDB detail web url or just a name

options:
  -h, --help     show this help message and exit
  --proxy PROXY  http proxy that uses, e.g. http://ip:port/token/
```
# sample
```shell
// 页面链接
> tmdb https://www.themoviedb.org/tv/155441
保存封面...
保存海报...
// 搜索
> tmdb 开端
0       电影    巴霍巴利王：开端
1       电视剧  开端
> 1
保存封面...
保存海报...
```
# build
> 编译以省去`python tmdb.py`

**编译之前可以修改proxy默认值省去每次加上**

终端运行`pyinstaller -F .\tmdb.spec`, 并将可执行文件添加到环境变量
