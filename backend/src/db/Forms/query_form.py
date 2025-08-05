"""
查询表单管理

使用SQLAlchemy重写，支持ORM和原生SQL两种方式

query_form 表结构：
┏━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━┓
┃ 字段名        ┃ 类型     ┃ 是否为空  ┃ 默认值  ┃ 主键  ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━┩
│ id           │ INTEGER │ 否       │ 自增   │ 是   │
│ lazy_query   │ TEXT    │ 是       │ NULL   │ 否   │
│ detail_query │ TEXT    │ 是       │ NULL   │ 否   │
│ creator_id   │ INTEGER │ 是       │ NULL   │ 否   │
│ priority     │ INTEGER │ 是       │ NULL   │ 否   │
│ created_at   │ TEXT    │ 否       │ NULL   │ 否   │
│ updated_at   │ TEXT    │ 是       │ NULL   │ 否   │
└──────────────┴─────────┴──────────┴────────┴──────┘

可用方法
add_query
delete_query
get_query_by_id
get_queries_by_creator
update_query
list_all_queries
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..base_form import BaseForm
from ..models import QueryModel

table_name = QueryModel.__tablename__

class QueryForm(BaseForm):
    """查询表单管理器 - SQLAlchemy版本"""

    def __init__(self, db_path="app.db"):
        super().__init__(db_path, table_name)

    def add_query(
        self, lazy_query: str = None, detail_query: str = None, 
        creator_id: int = None, priority: int = None
    ) -> bool:
        """添加查询 - 使用ORM方式"""
        try:
            session = self.Session()

            # 创建新查询
            new_query = QueryModel(
                lazy_query=lazy_query,
                detail_query=detail_query,
                creator_id=creator_id,
                priority=priority,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

            session.add(new_query)
            session.commit()

            console = Console()
            console.print(f"[green]✓ 查询添加成功！ID: {new_query.id}[/green]")
            session.close()
            return True

        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 添加查询失败: {e}[/red]")
            if "session" in locals():
                session.rollback()
                session.close()
            return False

    def get_query_by_id(self, query_id: int) -> QueryModel:
        """根据ID获取查询"""
        try:
            session = self.Session()
            query = session.query(QueryModel).filter_by(id=query_id).first()
            session.close()
            return query
        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 查询失败: {e}[/red]")
            return None

    def get_queries_by_creator(self, creator_id: int) -> list:
        """根据创建者ID获取查询列表"""
        try:
            session = self.Session()
            queries = session.query(QueryModel).filter_by(creator_id=creator_id).all()
            session.close()
            return queries
        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 查询失败: {e}[/red]")
            return []

    def update_query(self, query_id: int, **kwargs) -> bool:
        """更新查询信息"""
        try:
            session = self.Session()
            query = session.query(QueryModel).filter_by(id=query_id).first()

            if not query:
                console = Console()
                console.print(f"[red]✗ 查询 ID '{query_id}' 不存在[/red]")
                session.close()
                return False

            # 更新字段
            for key, value in kwargs.items():
                if hasattr(query, key):
                    setattr(query, key, value)

            # 设置更新时间
            query.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            session.commit()
            console = Console()
            console.print(f"[green]✓ 查询 ID '{query_id}' 更新成功！[/green]")
            session.close()
            return True

        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 更新查询失败: {e}[/red]")
            if "session" in locals():
                session.rollback()
                session.close()
            return False

    def delete_query(self, query_id: int) -> bool:
        """删除查询"""
        try:
            session = self.Session()
            query = session.query(QueryModel).filter_by(id=query_id).first()

            if not query:
                console = Console()
                console.print(f"[red]✗ 查询 ID '{query_id}' 不存在[/red]")
                session.close()
                return False

            session.delete(query)
            session.commit()

            console = Console()
            console.print(f"[green]✓ 查询 ID '{query_id}' 删除成功！[/green]")
            session.close()
            return True

        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 删除查询失败: {e}[/red]")
            if "session" in locals():
                session.rollback()
                session.close()
            return False

    def list_all_queries(self) -> list:
        """获取所有查询列表"""
        try:
            session = self.Session()
            queries = session.query(QueryModel).all()
            session.close()
            return queries
        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 获取查询列表失败: {e}[/red]")
            return []

    def display_queries(self):
        """显示所有查询信息"""
        queries = self.list_all_queries()

        if not queries:
            console = Console()
            console.print(
                Panel(
                    "[yellow]暂无查询数据[/yellow]",
                    title="查询列表",
                    border_style="yellow",
                )
            )
            return

        # 创建查询信息表格
        table = Table(title=f"查询列表 (共 {len(queries)} 个查询)")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("懒惰查询", style="green")
        table.add_column("详细查询", style="blue")
        table.add_column("创建者ID", style="magenta")
        table.add_column("优先级", style="yellow")
        table.add_column("创建时间", style="red")
        table.add_column("更新时间", style="white")

        for query in queries:
            table.add_row(
                str(query.id),
                query.lazy_query or "未设置",
                query.detail_query or "未设置",
                str(query.creator_id) if query.creator_id else "未设置",
                str(query.priority) if query.priority else "未设置",
                query.created_at,
                query.updated_at or "未更新",
            )

        console = Console()
        console.print(table) 