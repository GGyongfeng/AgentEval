"""
用户表单管理

使用SQLAlchemy重写，支持ORM和原生SQL两种方式

user_form 表结构：
┏━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━┓
┃ 字段名      ┃ 类型     ┃ 是否为空  ┃ 默认值  ┃ 主键  ┃
┡━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━┩
│ id         │ INTEGER │ 否       │ 自增   │ 是   │
│ username   │ TEXT    │ 否       │ NULL   │ 否   │
│ password   │ TEXT    │ 否       │ NULL   │ 否   │
│ nickname   │ TEXT    │ 否       │ NULL   │ 否   │
│ full_name  │ TEXT    │ 是       │ NULL   │ 否   │
│ created_at │ TEXT    │ 否       │ NULL   │ 否   │
│ updated_at │ TEXT    │ 是       │ NULL   │ 否   │
└────────────┴─────────┴──────────┴────────┴──────┘

可用方法
add_user
delete_user
get_user_by_username
update_user
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..base_form import BaseForm
from ..models import UserModel

class UserForm(BaseForm):
    """用户表单管理器 - SQLAlchemy版本"""

    def __init__(self, db_path="app.db"):
        super().__init__(db_path, UserModel)

    def add_user(
        self, username: str, password: str, nickname: str, full_name: str = None
    ) -> bool:
        """添加用户 - 使用ORM方式"""
        try:
            session = self.Session()

            # 检查用户名是否已存在
            existing_user = session.query(UserModel).filter_by(username=username).first()
            if existing_user:
                console = Console()
                console.print(f"[red]✗ 用户名 '{username}' 已存在[/red]")
                session.close()
                return False

            # 创建新用户
            new_user = UserModel(
                username=username,
                password=password,
                nickname=nickname,
                full_name=full_name,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

            session.add(new_user)
            session.commit()

            console = Console()
            console.print(f"[green]✓ 用户 '{username}' 添加成功！[/green]")
            session.close()
            return True

        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 添加用户失败: {e}[/red]")
            if "session" in locals():
                session.rollback()
                session.close()
            return False

    def get_user_by_username(self, username: str) -> UserModel:
        """根据用户名获取用户"""
        try:
            session = self.Session()
            user = session.query(UserModel).filter_by(username=username).first()
            session.close()
            return user
        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 查询用户失败: {e}[/red]")
            return None

    def update_user(self, username: str, **kwargs) -> bool:
        """更新用户信息"""
        try:
            session = self.Session()
            user = session.query(UserModel).filter_by(username=username).first()

            if not user:
                console = Console()
                console.print(f"[red]✗ 用户 '{username}' 不存在[/red]")
                session.close()
                return False

            # 更新字段
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            # 设置更新时间
            user.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            session.commit()
            console = Console()
            console.print(f"[green]✓ 用户 '{username}' 更新成功！[/green]")
            session.close()
            return True

        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 更新用户失败: {e}[/red]")
            if "session" in locals():
                session.rollback()
                session.close()
            return False

    def delete_user(self, username: str) -> bool:
        """删除用户"""
        try:
            session = self.Session()
            user = session.query(UserModel).filter_by(username=username).first()

            if not user:
                console = Console()
                console.print(f"[red]✗ 用户 '{username}' 不存在[/red]")
                session.close()
                return False

            session.delete(user)
            session.commit()

            console = Console()
            console.print(f"[green]✓ 用户 '{username}' 删除成功！[/green]")
            session.close()
            return True

        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 删除用户失败: {e}[/red]")
            if "session" in locals():
                session.rollback()
                session.close()
            return False