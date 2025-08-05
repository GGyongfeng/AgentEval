"""
文件表单管理

使用SQLAlchemy重写，支持ORM和原生SQL两种方式

files_form 表结构：
┏━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━┓
┃ 字段名        ┃ 类型     ┃ 是否为空  ┃ 默认值  ┃ 主键  ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━┩
│ id           │ INTEGER │ 否       │ 自增   │ 是   │
│ evaluation_id│ INTEGER │ 否       │ NULL   │ 否   │
│ filename     │ TEXT    │ 否       │ NULL   │ 否   │
│ content      │ BLOB    │ 是       │ NULL   │ 否   │
│ file_type    │ ENUM    │ 否       │ NULL   │ 否   │
│ file_size    │ INTEGER │ 是       │ NULL   │ 否   │
│ created_at   │ TEXT    │ 否       │ NULL   │ 否   │
│ updated_at   │ TEXT    │ 是       │ NULL   │ 否   │
└──────────────┴─────────┴──────────┴────────┴──────┘

文件类型枚举：
- trajectory: 轨迹文件
- report: 报告文件
- deliverable: 交付文件
- pre_data: 预处理数据

可用方法
add_file
delete_file
get_file_by_id
get_files_by_evaluation
get_files_by_type
update_file
list_all_files
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, LargeBinary, Enum
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..base_form import BaseForm
from ..models import FilesModel

table_name = FilesModel.__tablename__

class FilesForm(BaseForm):
    """文件表单管理器 - SQLAlchemy版本"""

    def __init__(self, db_path="app.db"):
        super().__init__(db_path, table_name)

    def add_file(
        self, evaluation_id: int, filename: str, file_type: str,
        content: bytes = None, file_size: int = None
    ) -> bool:
        """添加文件 - 使用ORM方式"""
        try:
            session = self.Session()

            # 验证文件类型
            valid_types = ["trajectory", "report", "deliverable", "pre_data"]
            if file_type not in valid_types:
                console = Console()
                console.print(f"[red]✗ 无效的文件类型: {file_type}[/red]")
                console.print(f"[yellow]有效类型: {', '.join(valid_types)}[/yellow]")
                session.close()
                return False

            # 创建新文件记录
            new_file = FilesModel(
                evaluation_id=evaluation_id,
                filename=filename,
                content=content,
                file_type=file_type,
                file_size=file_size,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

            session.add(new_file)
            session.commit()

            console = Console()
            console.print(f"[green]✓ 文件 '{filename}' 添加成功！ID: {new_file.id}[/green]")
            session.close()
            return True

        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 添加文件失败: {e}[/red]")
            if "session" in locals():
                session.rollback()
                session.close()
            return False

    def get_file_by_id(self, file_id: int) -> FilesModel:
        """根据ID获取文件"""
        try:
            session = self.Session()
            file_record = session.query(FilesModel).filter_by(id=file_id).first()
            session.close()
            return file_record
        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 查询失败: {e}[/red]")
            return None

    def get_files_by_evaluation(self, evaluation_id: int) -> list:
        """根据评估ID获取文件列表"""
        try:
            session = self.Session()
            files = session.query(FilesModel).filter_by(evaluation_id=evaluation_id).all()
            session.close()
            return files
        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 查询失败: {e}[/red]")
            return []

    def get_files_by_type(self, file_type: str) -> list:
        """根据文件类型获取文件列表"""
        try:
            session = self.Session()
            files = session.query(FilesModel).filter_by(file_type=file_type).all()
            session.close()
            return files
        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 查询失败: {e}[/red]")
            return []

    def update_file(self, file_id: int, **kwargs) -> bool:
        """更新文件信息"""
        try:
            session = self.Session()
            file_record = session.query(FilesModel).filter_by(id=file_id).first()

            if not file_record:
                console = Console()
                console.print(f"[red]✗ 文件 ID '{file_id}' 不存在[/red]")
                session.close()
                return False

            # 更新字段
            for key, value in kwargs.items():
                if hasattr(file_record, key):
                    setattr(file_record, key, value)

            # 设置更新时间
            file_record.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            session.commit()
            console = Console()
            console.print(f"[green]✓ 文件 ID '{file_id}' 更新成功！[/green]")
            session.close()
            return True

        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 更新文件失败: {e}[/red]")
            if "session" in locals():
                session.rollback()
                session.close()
            return False

    def delete_file(self, file_id: int) -> bool:
        """删除文件"""
        try:
            session = self.Session()
            file_record = session.query(FilesModel).filter_by(id=file_id).first()

            if not file_record:
                console = Console()
                console.print(f"[red]✗ 文件 ID '{file_id}' 不存在[/red]")
                session.close()
                return False

            session.delete(file_record)
            session.commit()

            console = Console()
            console.print(f"[green]✓ 文件 ID '{file_id}' 删除成功！[/green]")
            session.close()
            return True

        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 删除文件失败: {e}[/red]")
            if "session" in locals():
                session.rollback()
                session.close()
            return False

    def list_all_files(self) -> list:
        """获取所有文件列表"""
        try:
            session = self.Session()
            files = session.query(FilesModel).all()
            session.close()
            return files
        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 获取文件列表失败: {e}[/red]")
            return []

    def display_files(self):
        """显示所有文件信息"""
        files = self.list_all_files()

        if not files:
            console = Console()
            console.print(
                Panel(
                    "[yellow]暂无文件数据[/yellow]",
                    title="文件列表",
                    border_style="yellow",
                )
            )
            return

        # 创建文件信息表格
        table = Table(title=f"文件列表 (共 {len(files)} 个文件)")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("评估ID", style="green")
        table.add_column("文件名", style="blue")
        table.add_column("文件类型", style="magenta")
        table.add_column("文件大小(字节)", style="yellow")
        table.add_column("是否有内容", style="red")
        table.add_column("创建时间", style="white")
        table.add_column("更新时间", style="cyan")

        for file_record in files:
            has_content = "是" if file_record.content else "否"
            file_size_str = str(file_record.file_size) if file_record.file_size else "未设置"
            
            table.add_row(
                str(file_record.id),
                str(file_record.evaluation_id),
                file_record.filename,
                file_record.file_type,
                file_size_str,
                has_content,
                file_record.created_at,
                file_record.updated_at or "未更新",
            )

        console = Console()
        console.print(table)

    def get_file_content(self, file_id: int) -> bytes:
        """获取文件内容"""
        try:
            session = self.Session()
            file_record = session.query(FilesModel).filter_by(id=file_id).first()
            session.close()
            
            if file_record and file_record.content:
                return file_record.content
            else:
                console = Console()
                console.print(f"[red]✗ 文件 ID '{file_id}' 不存在或没有内容[/red]")
                return None
        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 获取文件内容失败: {e}[/red]")
            return None 