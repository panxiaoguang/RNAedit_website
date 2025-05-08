# RNAedit_website

## 如何部署

### 1. 安装数据库
本项目使用的是 PostgreSQL 数据库，所以需要预先配置好数据库。数据库配置完毕后，新建数据库，命令大概长这样：
首先启动数据库：
```
sudo service postgresql start
```
如果你使用的是 conda 安装的 PostgreSQL，那么启动步骤可能是：

```
initdb -D ~/my_pgdata
pg_ctl -D ~/my_pgdata -l logfile start
```

登录数据库：
```
psql -U postgres
```

新建数据库：
```
CREATE DATABASE reflexdb;
```

为默认用户 postgres 设置密码:

```
ALTER USER postgres WITH PASSWORD 'admin';
```

退出psql 

接下来要配置公开访问，因为构建docker 过程中需要该 DB_URL 链接，而 Docker 无法直接和宿主机通讯。
更改配置文件：
修改`postgresql.conf`文件，添加以下内容：
```
listen_addresses = '*'
```
修改`pg_hba.conf`文件，添加以下内容：

```
##注意不要有···中间是tab 分割
host    all             all             0.0.0.0/0               md5
```

重启数据库：
```
sudo service postgresql restart
```
conda 安装的数据库重启命令是：
```
pg_ctl -D ~/my_pgdata -l logfile restart
```
最后，我们的数据库的本地访问链接为：
```
postgresql://postgres:admin@localhost:5432/reflexdb
```
而公开访问链接为
```
postgresql://postgres:admin@<Your-IP>:5432/reflexdb
```
### 2. 上传数据到数据库

克隆本仓库到本地目录

```bash
git clone https://github.com/panxiaoguang/RNAedit_website.git
cd RNAedit_website
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

修改 `rxconfig.py`文件，添加`db_url`到配置文件中。

```python
config = rx.Config(
    app_name="MAIRE",
    show_built_with_reflex=False, ## to remove the badge
    db_url="postgresql://postgres:admin@<your-ip-address>:5432/reflexdb",
    tailwind={
        "theme": {
            "extend": {
            },
        },
        "plugins": ["@tailwindcss/typography"],
    },
)
```

然后初始化项目同时初始化数据库：

```bash
reflex init
reflex db init
reflex db makemigrations --message 'something changed'
reflex db migrate
```

运行项目下的`upload_data_to_database.py`文件，上传数据到数据库。

需要修改脚本内的以下内容：

- daba_path: 数据文件所在的路径
- data_files: 数据文件的名称列表

所有的数据文件可以从该链接获取：
[https://sid.erda.dk/cgi-sid/ls.py?share_id=ehwzuQDtFN](https://sid.erda.dk/cgi-sid/ls.py?share_id=ehwzuQDtFN)

```python
if __name__ == "__main__":
    data_path = "<your_maire_data_path>"
    data_files = [
        "Gene_data_Macaque.txt",
        "repeats.tsv",
        "tissues.tsv",
        "AA_changes.tsv",
        "RNA_editing_data.txt",
        "RE_levels.tsv",
    ]
```

```bash
python upload_data_to_database.py
```

### 3. 构建 Docker 镜像并运行

等所有数据上传完毕后，就可以运行项目了，端口 7900 可以改成任意的端口即可
修改 `rxconfig.py`文件，删除`db_url`，因为我们用`--build-arg` 来传入
```bash
### 构建镜像
docker pull xiaohanys91/rnaedit:1.0.4

### 运行镜像
docker run -d -p 62001:62001 xiaohanys91/rnaedit:1.0.4
```


此时，网站已经可以在http://localhost:7900上访问了。
