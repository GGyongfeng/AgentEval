"""
抽象基类 - 表单管理基类

所有表单管理类都应该继承这个基类
使用SQLAlchemy重写，逻辑不变
"""

from abc import ABC, abstractmethod
from math import degrees
from typing import Type
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .models import Base

console = Console()

class BaseForm(ABC):
    
    def __init__(self, db_path:str, table_Model: Type[Base]):
        self.db_path = db_path
        self.model = table_Model
        self.table_name = table_Model.__tablename__
        
        # 创建SQLAlchemy引擎和会话
        self.engine = create_engine(f'sqlite:///{self.db_path}', echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def _create_tables(self) -> bool:
        """创建Base 绑定的所有表 - 使用ORM"""
        try:
            # 方式1: 使用SQLAlchemy ORM创建表
            # 绑定Base到引擎
            Base.metadata.bind = self.engine
            # 创建所有表
            Base.metadata.create_all(self.engine)
            console = Console()
            console.print(
                f"[green]✓ all Forms 绑定到 {self.db_path} 成功！(使用ORM)[/green]"
            )
            return True
        except SQLAlchemyError as e:
            # 方式2: 回退到原生SQL方式
            console = Console()
            console.print(f"[yellow]ORM创建失败，尝试使用原生SQL: {e}[/yellow]")
            return False
    
    def get_structure(self):
        """获取表信息 - 通用方法"""
        try:
            inspector = inspect(self.engine)
            
            # 检查表是否存在
            if self.table_name not in inspector.get_table_names():
                return None
            
            # 获取表结构
            columns = inspector.get_columns(self.table_name)
            pk_constraint = inspector.get_pk_constraint(self.table_name)
            pk_columns = pk_constraint.get('constrained_columns', [])
            
            # 转换为原格式 (cid, name, type, not_null, default_val, pk)
            formatted_columns = []
            for i, col in enumerate(columns):
                formatted_columns.append([
                    i,  # cid
                    col['name'],  # name
                    str(col['type']),  # type
                    str(col['nullable']),  # nullable
                    col.get('default'),  # default_val
                    1 if col['name'] in pk_columns else 0  # pk
                ])
            
            # 获取行数
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {self.table_name}"))
                row_count = result.scalar()
            
            return {
                'columns': formatted_columns,
                'row_count': row_count
            }
            
        except SQLAlchemyError as e:
            console.print(f"[red]✗ 获取表信息失败: {e}[/red]")
            return None
    
    def display_structure(self):
        """展示表信息 - 通用方法"""
        info = self.get_structure()
        
        if not info:
            console.print(Panel(
                f"[yellow]表 '{self.table_name}' 不存在[/yellow]",
                title="表状态",
                border_style="yellow"
            ))
            return
        
        # 创建表结构信息表格
        structure_table = Table(title=f"表 '{self.table_name}' 结构信息")
        structure_table.add_column("字段名", style="cyan", no_wrap=True)
        structure_table.add_column("类型", style="green")
        structure_table.add_column("nullable", style="yellow")
        structure_table.add_column("默认值", style="blue")
        structure_table.add_column("主键", style="red")
        
        for col in info['columns']:
            cid, name, type_name, not_null, default_val, pk = col
            structure_table.add_row(
                name,
                type_name,
                not_null,
                str(default_val) if default_val else "NULL",
                "是" if pk else "否"
            )
        
        # 创建统计信息
        stats_table = Table.grid(padding=1)
        stats_table.add_column("属性", style="cyan", no_wrap=True)
        stats_table.add_column("值", style="white")
        
        stats_table.add_row("表名", self.table_name)
        stats_table.add_row("字段数", str(len(info['columns'])))
        stats_table.add_row("行数", str(info['row_count']))
        
        # 显示信息
        console.print(Panel(
            stats_table,
            title=f"[bold blue]表 '{self.table_name}' 统计信息[/bold blue]",
            border_style="blue"
        ))
        
        console.print(structure_table)
    
    def get_lines(self):
        """获取所有行"""
        try:
            session = self.Session()
            models = session.query(self.model).all()
            session.close()
            return models
        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 获取评估列表失败: {e}[/red]")
            return []
    
    def display_lines(self):
        """显示表的所有列"""
        queries = self.get_lines()

        console = Console()
        if not queries:
            console.print(
                Panel("[yellow]暂无数据[/yellow]", title="列表", border_style="yellow")
            )
            return

        # 自动获取列名
        table = Table(title=f"{self.model.__tablename__} (共 {len(queries)} 条)")
        for col in self.model.__table__.columns:
            table.add_column(col.name, style="cyan")

        # 遍历所有行，按字段值填入
        for item in queries:
            values = []
            for col in self.model.__table__.columns:
                value = getattr(item, col.name)
                if value is None or value == "":
                    value = "未设置"
                else:
                    value = str(value)
                values.append(value)
            table.add_row(*values)

        console.print(table)

    def __del__(self):
        """析构函数，确保连接被正确关闭"""
        if hasattr(self, 'engine'):
            self.engine.dispose()

def main():
    base_form = BaseForm("app.db", "默认表")
    base_form._create_tables()
    base_form.display_table_info()

if __name__ == "__main__":
    main()