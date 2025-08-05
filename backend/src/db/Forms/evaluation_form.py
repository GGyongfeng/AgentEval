"""
评估表单管理

使用SQLAlchemy重写，支持ORM和原生SQL两种方式

evaluation_form 表结构：
┏━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━┓
┃ 字段名        ┃ 类型     ┃ 是否为空  ┃ 默认值  ┃ 主键  ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━┩
│ id           │ INTEGER │ 否       │ 自增   │ 是   │
│ query_id     │ INTEGER │ 否       │ NULL   │ 否   │
│ agent        │ TEXT    │ 是       │ NULL   │ 否   │
│ evaluator_id │ INTEGER │ 是       │ NULL   │ 否   │
│ quality_score│ INTEGER │ 是       │ NULL   │ 否   │
│ trajectory   │ TEXT    │ 是       │ NULL   │ 否   │
│ report_content│ TEXT   │ 是       │ NULL   │ 否   │
│ created_at   │ TEXT    │ 否       │ NULL   │ 否   │
│ updated_at   │ TEXT    │ 是       │ NULL   │ 否   │
└──────────────┴─────────┴──────────┴────────┴──────┘

可用方法
add_evaluation
delete_evaluation
get_evaluation_by_id
get_evaluations_by_query
get_evaluations_by_evaluator
update_evaluation
list_all_evaluations
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..base_form import BaseForm
from ..models import EvaluationModel

table_name = EvaluationModel.__tablename__

class EvaluationForm(BaseForm):
    """评估表单管理器 - SQLAlchemy版本"""

    def __init__(self, db_path="app.db"):
        super().__init__(db_path, table_name)

    def add_evaluation(
        self, query_id: int, agent: str = None, evaluator_id: int = None,
        quality_score: int = None, trajectory: str = None, report_content: str = None,
        deliverables: list = None
    ) -> bool:
        """添加评估 - 支持同时添加若干交付文件（deliverable），并通过FilesForm.add_file方法写入"""
        from .files_form import FilesForm
        try:
            session = self.Session()

            # 创建新评估
            new_evaluation = EvaluationModel(
                query_id=query_id,
                agent=agent,
                evaluator_id=evaluator_id,
                quality_score=quality_score,
                trajectory=trajectory,
                report_content=report_content,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

            session.add(new_evaluation)
            session.flush()  # 获取new_evaluation.id

            # 批量添加交付文件
            if deliverables:
                if not isinstance(deliverables, list):
                    raise ValueError("deliverables 必须为 list")
                files_form = FilesForm(self.db_path)
                for file in deliverables:
                    if not isinstance(file, dict):
                        raise ValueError("每个交付文件必须为 dict")
                    filename = file.get("filename")
                    content = file.get("content")
                    file_size = file.get("file_size")
                    if not isinstance(filename, str):
                        raise ValueError("filename 必须为字符串")
                    if not isinstance(content, bytes):
                        raise ValueError("content 必须为二进制 bytes")
                    # 通过FilesForm.add_file方法添加
                    ok = files_form.add_file(
                        evaluation_id=new_evaluation.id,
                        filename=filename,
                        file_type="deliverable",
                        content=content,
                        file_size=file_size
                    )
                    if not ok:
                        raise RuntimeError(f"添加文件 {filename} 失败")

            session.commit()

            console = Console()
            console.print(f"[green]✓ 评估添加成功！ID: {new_evaluation.id}，交付文件数: {len(deliverables) if deliverables else 0}[/green]")
            session.close()
            return True

        except (SQLAlchemyError, ValueError, RuntimeError) as e:
            console = Console()
            console.print(f"[red]✗ 添加评估及交付文件失败: {e}[/red]")
            if "session" in locals():
                session.rollback()
                session.close()
            return False

    def get_evaluation_by_id(self, evaluation_id: int) -> EvaluationModel:
        """根据ID获取评估"""
        try:
            session = self.Session()
            evaluation = session.query(EvaluationModel).filter_by(id=evaluation_id).first()
            session.close()
            return evaluation
        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 查询失败: {e}[/red]")
            return None

    def get_evaluations_by_query(self, query_id: int) -> list:
        """根据查询ID获取评估列表"""
        try:
            session = self.Session()
            evaluations = session.query(EvaluationModel).filter_by(query_id=query_id).all()
            session.close()
            return evaluations
        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 查询失败: {e}[/red]")
            return []

    def get_evaluations_by_evaluator(self, evaluator_id: int) -> list:
        """根据评估者ID获取评估列表"""
        try:
            session = self.Session()
            evaluations = session.query(EvaluationModel).filter_by(evaluator_id=evaluator_id).all()
            session.close()
            return evaluations
        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 查询失败: {e}[/red]")
            return []

    def update_evaluation(self, evaluation_id: int, **kwargs) -> bool:
        """更新评估信息"""
        try:
            session = self.Session()
            evaluation = session.query(EvaluationModel).filter_by(id=evaluation_id).first()

            if not evaluation:
                console = Console()
                console.print(f"[red]✗ 评估 ID '{evaluation_id}' 不存在[/red]")
                session.close()
                return False

            # 更新字段
            for key, value in kwargs.items():
                if hasattr(evaluation, key):
                    setattr(evaluation, key, value)

            # 设置更新时间
            evaluation.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            session.commit()
            console = Console()
            console.print(f"[green]✓ 评估 ID '{evaluation_id}' 更新成功！[/green]")
            session.close()
            return True

        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 更新评估失败: {e}[/red]")
            if "session" in locals():
                session.rollback()
                session.close()
            return False

    def delete_evaluation(self, evaluation_id: int) -> bool:
        """删除评估"""
        try:
            session = self.Session()
            evaluation = session.query(EvaluationModel).filter_by(id=evaluation_id).first()

            if not evaluation:
                console = Console()
                console.print(f"[red]✗ 评估 ID '{evaluation_id}' 不存在[/red]")
                session.close()
                return False

            session.delete(evaluation)
            session.commit()

            console = Console()
            console.print(f"[green]✓ 评估 ID '{evaluation_id}' 删除成功！[/green]")
            session.close()
            return True

        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 删除评估失败: {e}[/red]")
            if "session" in locals():
                session.rollback()
                session.close()
            return False

    def list_all_evaluations(self) -> list:
        """获取所有评估列表"""
        try:
            session = self.Session()
            evaluations = session.query(EvaluationModel).all()
            session.close()
            return evaluations
        except SQLAlchemyError as e:
            console = Console()
            console.print(f"[red]✗ 获取评估列表失败: {e}[/red]")
            return []

    def display_evaluations(self):
        """显示所有评估信息"""
        evaluations = self.list_all_evaluations()

        if not evaluations:
            console = Console()
            console.print(
                Panel(
                    "[yellow]暂无评估数据[/yellow]",
                    title="评估列表",
                    border_style="yellow",
                )
            )
            return

        # 创建评估信息表格
        table = Table(title=f"评估列表 (共 {len(evaluations)} 个评估)")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("查询ID", style="green")
        table.add_column("代理", style="blue")
        table.add_column("评估者ID", style="magenta")
        table.add_column("质量分数", style="yellow")
        table.add_column("轨迹", style="red")
        table.add_column("报告内容", style="white")
        table.add_column("创建时间", style="cyan")
        table.add_column("更新时间", style="green")

        for evaluation in evaluations:
            # 截断长文本以便显示
            trajectory_preview = evaluation.trajectory[:50] + "..." if evaluation.trajectory and len(evaluation.trajectory) > 50 else evaluation.trajectory or "未设置"
            report_preview = evaluation.report_content[:50] + "..." if evaluation.report_content and len(evaluation.report_content) > 50 else evaluation.report_content or "未设置"
            
            table.add_row(
                str(evaluation.id),
                str(evaluation.query_id),
                evaluation.agent or "未设置",
                str(evaluation.evaluator_id) if evaluation.evaluator_id else "未设置",
                str(evaluation.quality_score) if evaluation.quality_score else "未设置",
                trajectory_preview,
                report_preview,
                evaluation.created_at,
                evaluation.updated_at or "未更新",
            )

        console = Console()
        console.print(table) 