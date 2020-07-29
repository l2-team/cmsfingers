# CMS指纹字典
## 搜集国内/外常见CMS指纹
____
> 有提交字典的，可以提issue或者发我
> 字典慢慢更新
> 部分指纹上传之后会更新一个多线程扫描脚本

### CMS 格式
+ `cms` cms名字, 英文小写
+ `file_type` 文件类型
+ `match_pattern` md5/patten/keyword
+ `path` 路径
+ `type` 类型
+ `uptime` 更新时间/增添时间
```json
{
    "cms": "dedecms",
    "file_type": "css",
    "type": "md5/patten/keyword",
    "match_pattern": "[md5值]",
    "path": "/public/static/css/style.css",
    "uptime": "2019-05-21 19:03:43"
}
```

#### 批量扫描脚本使用
```shell
➜  cmsfingers git:(master) python3 finger.py -h
Usage: finger.py -u "http://xxxx.com" -t threads_number

Options:
  -h, --help            show this help message and exit
  -u URL, --url=URL     目标URL
  -f FILE, --file=FILE  url文件
  -t THREADS, --threads=THREADS
                        线程大小, 默认为 10
```
+ `-u` 目标URL
+ `-f` 目标URL文件
+ `-t` 线程


### 已更新记录
+ 2020年07月20日 更新 `200`个CMS, 指纹数量共 `997`个
+ 2020年07月22日 目前共 `200`个CMS, 指纹数量共 `1493`个
+ 2020年07月28日 目前共 `300`个, 指纹数量共 `1982`个
+ 更新脚本, 带上 `-f` 参数