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


## sherpa-ncnn在树莓派上运行

### linux（ubuntu）安装cmake等

#### 网站：根据版本和系统号调整

```
https://cmake.org/files/v3.20/cmake-3.20.0-linux-x86_64.tar.gz
```

#### 解压缩：

```
tar xf cmake-3.20.0-linux-x86_64.tar.gz
```

#### 添加全局变量：

```
export PATH="/home/ubuntu/cmake-3.20.0-linux-x86_64/bin:$PATH"
```

#### 检查安装情况：

```
which cmake
cmake --version
```

### ubutu安装交叉编译环境（目标树莓派arm32）

#### 查看目标-树莓派情况

```
uname -a   # armv7l是32位系统
ls /bin/ls # 32-bit LSB executable, ARM, EABI5 version 1
```

#### 安装对应的32位arm

[参考链接](https://k2-fsa.github.io/sherpa/ncnn/install/arm-embedded-linux.html)

```
mkdir -p $HOME/software
cd $HOME/software
wget https://huggingface.co/csukuangfj/sherpa-ncnn-toolchains/resolve/main/gcc-arm-8.3-2019.03-x86_64-arm-linux-gnueabihf.tar.xz
tar xvf gcc-arm-8.3-2019.03-x86_64-arm-linux-gnueabihf.tar.xz
```

编译且检查：变量关掉终端后需重新添加

```
export PATH=$HOME/software/gcc-arm-8.3-2019.03-x86_64-arm-linux-gnueabihf/bin:$PATH
arm-linux-gnueabihf-gcc --version
```

### ubutu上编译sherpa-ncnn

```
git clone https://github.com/k2-fsa/sherpa-ncnn
cd sherpa-ncnn
./build-arm-linux-gnueabihf.sh
```

可能第一次不成功

得到如下文件：

```
$ ls -lh  build-arm-linux-gnueabihf/install/bin/

total 6.6M
-rwxr-xr-x 1 kuangfangjun root 2.2M Jan 14 21:46 sherpa-ncnn
-rwxr-xr-x 1 kuangfangjun root 2.2M Jan 14 21:46 sherpa-ncnn-alsa
```

### ubuntu上下载模型

中英混合模型：

```
sudo apt-get install git-lfs   # git插件
```

```
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/csukuangfj/sherpa-ncnn-conv-emformer-transducer-2022-12-06
cd sherpa-ncnn-conv-emformer-transducer-2022-12-06
git lfs pull --include "*.bin"
```

完成之后查看得到：

```
ubuntu@VM-12-13-ubuntu:~/software/sherpa-ncnn-conv-emformer-transducer-2022-12-06$ ls -lh {encoder,decoder,joiner}*
-rw-rw-r-- 1 ubuntu ubuntu 5.9M Jan 28 13:51 decoder_jit_trace-pnnx.ncnn.bin
-rw-rw-r-- 1 ubuntu ubuntu  439 Jan 28 13:46 decoder_jit_trace-pnnx.ncnn.param
-rw-rw-r-- 1 ubuntu ubuntu 142M Jan 28 14:28 encoder_jit_trace-pnnx.ncnn.bin
-rw-rw-r-- 1 ubuntu ubuntu  99M Jan 28 14:02 encoder_jit_trace-pnnx.ncnn.int8.bin
-rw-rw-r-- 1 ubuntu ubuntu  78K Jan 28 13:46 encoder_jit_trace-pnnx.ncnn.int8.param
-rw-rw-r-- 1 ubuntu ubuntu  79K Jan 28 13:46 encoder_jit_trace-pnnx.ncnn.param
-rw-rw-r-- 1 ubuntu ubuntu 7.0M Jan 28 13:51 joiner_jit_trace-pnnx.ncnn.bin
-rw-rw-r-- 1 ubuntu ubuntu 3.5M Jan 28 13:51 joiner_jit_trace-pnnx.ncnn.int8.bin
-rw-rw-r-- 1 ubuntu ubuntu  498 Jan 28 13:46 joiner_jit_trace-pnnx.ncnn.int8.param
-rw-rw-r-- 1 ubuntu ubuntu  490 Jan 28 13:46 joiner_jit_trace-pnnx.ncnn.p
```
