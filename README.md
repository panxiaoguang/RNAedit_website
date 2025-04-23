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

退出psql 后重启数据库：
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
    db_url="postgresql://postgres:admin@localhost:5432/reflexdb",
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

```python
if __name__ == "__main__":
    data_path = "/home/panxiaoguang/Projects/maire_data"
    data_files = [
        "sample_Gene_data_Macaque.txt",
        "repeats.tsv",
        "tissues.tsv",
        "AA_changes.tsv",
        "sample_RNA_editing_data.txt",
        "sample_RE_levels.tsv",
    ]
```

```bash
python upload_data_to_database.py
```

### 3. 构建 Docker 镜像并运行

等所有数据上传完毕后，就可以运行项目了，端口 7900 可以改成任意的端口即可

```bash
### 构建镜像
docker build --build-arg PORT=7900 --build-arg DB_URL=postgresql://postgres:admin@localhost:5432/reflexdb -t MAIRE .

### 运行镜像
docker push -d -p 7900:7900 MAIRE
```


此时，网站已经可以在http://localhost:7900上访问了。
