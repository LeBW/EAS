# EAS
教务系统抢课脚本。暂支持【南京大学，同济大学】。

> 需使用 Python3

## 南京大学
首先需要安装python相关包
```bash
pip3 install requests
pip3 install configparser
pip3 install beautifulsoup4
```
然后运行相关脚本，按照提升操作
```
python3 nju_eas.py
```

## 同济大学
适用于同济大学第三四轮抢课。

### 环境配置
首先需要安装python的自动化测试框架`selenium`
```
pip3 install selenium
```

然后需要安装Chrome以及Chrome Driver.
> Chrome 与 Chrome Driver的版本需要完全对应。

* 首先进入[Chrome官网](https://www.google.cn/intl/zh-CN/chrome/)安装Chrome。
* 打开 Chrome，进入 设置->关于，查看 Chrome 版本。
* 进入淘宝提供的 [Chrome Driver Mirror](http://npm.taobao.org/mirrors/chromedriver/)，进入对应版本的文件夹，下载相应的Chrome Driver。
* 下载解压后，将 `chromedriver`可执行文件所在目录放进环境变量`PATH`中。
* 在终端中输入`chromedriver`进行测试，如果开始执行，则配置完毕。

### 运行脚本
以上配置完成后，执行
```
python3 tongji_eas.py
```
* 开始执行后，脚本会自动打开一个浏览器页面，进入教务系统。
* 在其中登陆自己的账户，进入选课页面，同时选中想要抢的课。
* 看准自己想选的课的老师排第几个，例如排第3个，就在终端中输入3，并点击回车。
* 脚本会开始自动抢课，直至抢中。