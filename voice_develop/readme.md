### voice与text相互转换

#### 1：百度api

很简单，只需获得token id，再post即可，详情见各个文件夹。

缺点：时间

#### 2：speechrecognition库

是py的三方库，本质上是调用的谷歌api，但无需密码，应该更快。

缺点：单纯的库工作原理是调用api，树莓派不翻墙会超时

recognize_sphinx是唯一一个离线的，但很慢（5秒）且识别率低

#### ３：spchcat

下载后直接安装，报错：

```shell
spchcat:error while loading shared libraries: libhello.so.3: cannot open shared object file: No such file or directory
```

好像是软链接的问题，解决方法是：

```shell
sudo apt-get install libsox-dev
```

通过 ``sudo spt-get install spchcat``安装的都在 ``/usr/local/bin``中，查找安装的 ``spchcat``所需要的依赖语句wei:``ldd /usr/local/bin/spchcat``.

sb玩意不支持中文！！！白费我两小时，艹

#### 4：Porcupine热词唤醒


### 树莓派pip装库

#### 1：改默认下载路径

```shell
sudo nano /etc/pip.conf
```

替换如下:

```shell
extra-index-url=https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 2：下载whl库文件，手动安装

```shell
pip3 install xxx.whl
```

下载链接：

```shell
https://www.piwheels.org/simple/
```
