# 数据库管理脚本

这个目录包含了用于管理 SQLite 数据库的 Python 脚本。

## 文件说明

- `database.py` - 主数据库管理脚本，用于检查/创建数据库并展示数据库信息
- `base_form.py` - 抽象基类，提供通用的表单管理功能
- `XXX_form.py` - 各个表单
- `requirements.txt` - Python 依赖包列表

## 架构设计

### BaseForm 抽象基类

`BaseForm` 是一个抽象基类，提供了以下功能：

- **通用方法**：
  - `get_table_info()` - 获取表信息
  - `display_table_info()` - 美观展示表信息
  - `execute_create_table()` - 执行创建表的通用逻辑

- **抽象方法**（子类必须实现）：
  - `get_table_name()` - 返回表名
  - `create_table()` - 创建表的具体逻辑
  - `get_table_schema()` - 返回表的SQL创建语句

### 创建新的表单类

要创建新的表单类，只需要继承 `BaseForm` 并实现抽象方法：

```python
from base_form import BaseForm

class MyFormManager(BaseForm):
    def get_table_name(self) -> str:
        return 'my_form'
    
    def get_table_schema(self) -> str:
        return '''
            CREATE TABLE IF NOT EXISTS my_form (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        '''
    
    def create_table(self) -> bool:
        return False
```

## 使用方法

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 创建数据库

```bash
python database.py
```

这个脚本会：
- 检查数据库是否存在
- 如果不存在，创建数据库
- 使用 rich 库美观展示数据库信息

### 3. 创建表

```bash
python XXX_form.py
```

这个脚本会：
- 检查表是否存在
- 如果不存在，创建表
- 展示表的结构信息和统计信息

## 注意事项

- 所有脚本都使用 `app.db` 作为默认数据库文件名
- 脚本会自动处理表已存在的情况，不会重复创建
- 使用 rich 库提供美观的命令行界面展示
- 所有表单类都继承自 `BaseForm`，确保代码的一致性和可维护性 