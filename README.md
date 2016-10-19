## Flask Rss Feeder and bookmark

* Simple RSS Feeder based on Flask



---

* Run on Terminal 
    * $ pyvenv venv
    * $ source venv/bin/activate.fish
    * or
    * $ source venv/bin/activate
    * activated  the virtual environment of python 3.5.
    * $ pip install --upgrade pip
    * $ pip install -r requirements.txt
    * 如果requirements 一次失败，请多次执行，国内网络原因
    * $ python db_create.py
    * $ python db_migrate.py
    * & python db_upgrade.py
    * $ python run.py


---

* IDE: PyCharm

* 局域网内成员均可使用.
    * 查看开启服务机ip
    * $ ifconfig

* 浏览器输入: 
    * http://192.168.xx.xx:5000/
   
---

## RSS TEST

* http://blog.sina.com.cn/rss/1286528122.xml
* http://blog.sina.com.cn/rss/twocold.xml
* http://feed.williamlong.info/
* http://36kr.com/feed/


---
## @author

* changcheng

---

Upgrade
=======

This is done by running: `python db_migrate && python db_upgrade`. 


After the introduction of feeds, the whole bookmark model was renamed and extended. Due to this a script called 'db_merge.py' was created. This upgrade is done by;
  * Move the current flaskmarks.sqlite file to something like flaskmarks.sqlite.old. (A good practice is also to take an backup)
  * Run `python db_create.py` (this creates a new flaskmarks.sqlite file)
  * Run `python db_merge.py flaskmarks.sqlite.old flaskmarks.sqlite`
This process runs trough the old database and copies it into the new. It is therefor important that the flaskmarks.sqlite does not contain anything other than the schema.


--- 
## @log
* v2.1
    1. 规范化代码(PEP8)
    2. 全面python3 (3.5)
    3. 舍弃py2 的代码
* v2.0
    1. 重构整个项目
    2. 各个模块更加独立
    3. RSS 源访问正常
* v1.0
    1. bookmark 功能实现
    2. UI 完善
* v0.5
    1. templates 文件结构转变
    2. 增加推荐标签
    3. 增加最近添加标签
* v0.4
    1. 添加了css 的样式
    2. 优化登陆界面
    3. 优化UI
    4. search 功能完成
* v0.3
    1. User Register successful
    2. 改善框架
* v0.2
    1. User Login successful
    2. Templates 框架完成
* v0.1
    1. 初始化工程
