# crawlergo子域名式漏洞扫描

使用如下的原项目修改而来，主要是修改了目标来源，利用ESD来获取子域名，验证子域名并简单去重，通过crawlergo来爬取域名地址，交给xray来扫描，最后由slack通知。安装手机app即可接收信息，随时随地发现漏洞。

https://github.com/timwhitez/crawlergo_x_XRAY

https://github.com/0Kee-Team/crawlergo

#### crawlergo配置

配置请查看官方的配置信息，若运行如下可以爬取到链接，则可以正常使用crawlergo，如果出现异常，请根据官方提示解决。

```
./crawlergo -c ./crawler/chrome-linux/chrome -t 5 http://testphp.vulnweb.com
```

#### xray 配置

下载官方Linux版，因为ESD只能再Linux下运行，所以需要Linux主机。

开启一个监听，运行文件中的app.py，使用flask编写。做一个后台监听即可，同时需要修改app.py中的slack监听接口。类似https://hooks.slack.com/services/xxxxx/xxxx/xxxxxx

https://api.slack.com/apps创建一个app，申请一个**Webhook URL**。

```
flask run
```

配置开启后，还需要做一个xray监听的后台进程，监听浏览器的数据，扫描后由flask接口处理发送。

```
./xray webscan --listen 127.0.0.1:7777 --webhook-output http://127.0.0.1:5000/webhook
```

### 程序运行

配置后，需要一个定时任务，比如七天运行一次。注意文件权限

```
0 0 */7 * * cd /home/test/crawlergo_sub && /home/test/anaconda3/bin/python /home/test/crawlergo_sub/launcher_new.py >> /var/log/crawlergo.log
```

在subdomain文件夹下，domain是根域名文件，需要先配置根域名。内部都是配置的五个标签页，如果情况适合，可以适当添加。

#### 第三方模块

```
ESD
requests
simplejson	
flask
```

