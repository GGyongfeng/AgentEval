"""
数据库初始化 - SQLAlchemy版本
"""
import os
from datetime import datetime
from sqlalchemy import create_engine, MetaData, inspect, text
from sqlalchemy.orm import sessionmaker
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

class DatabaseManager:
    def __init__(self, db_path='app.db'):
        self.db_path = db_path
        self.engine = None
        self.Session = None
        self.metadata = MetaData()
        
    def get_database_url(self):
        """获取数据库URL"""
        return f"sqlite:///{self.db_path}"
    
    def is_database_exists(self):
        """检查数据库是否存在"""
        return os.path.exists(self.db_path)
    
    def create_database(self):
        """创建数据库"""
        try:
            self.engine = create_engine(self.get_database_url(), echo=False)
            self.Session = sessionmaker(bind=self.engine)
            
            # 创建所有表
            self.metadata.create_all(self.engine)
            
            console.print(f"[green]✓ 数据库 '{self.db_path}' 创建成功！[/green]")
            return True
        except Exception as e:
            console.print(f"[red]✗ 创建数据库失败: {e}[/red]")
            return False
    
    def get_database_info(self):
        """获取数据库信息"""
        if not self.is_database_exists():
            return None
            
        try:
            self.engine = create_engine(self.get_database_url(), echo=False)
            inspector = inspect(self.engine)
            
            # 获取数据库文件信息
            file_stat = os.stat(self.db_path)
            file_size = file_stat.st_size
            created_time = datetime.fromtimestamp(file_stat.st_ctime)
            modified_time = datetime.fromtimestamp(file_stat.st_mtime)
            
            # 获取表信息
            tables = inspector.get_table_names()
            
            # 获取每个表的行数
            table_info = []
            for table_name in tables:
                with self.engine.connect() as conn:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                    row_count = result.scalar()
                    table_info.append((table_name, row_count))
            
            return {
                'file_size': file_size,
                'created_time': created_time,
                'modified_time': modified_time,
                'tables': table_info
            }
            
        except Exception as e:
            console.print(f"[red]✗ 获取数据库信息失败: {e}[/red]")
            return None
    
    def display_database_info(self):
        """使用rich库美观展示数据库信息"""
        if not self.is_database_exists():
            console.print(Panel(
                "[yellow]数据库不存在，正在创建...[/yellow]",
                title="数据库状态",
                border_style="yellow"
            ))
            if self.create_database():
                console.print(Panel(
                    "[green]数据库创建完成！[/green]",
                    title="创建结果",
                    border_style="green"
                ))
            return
        
        info = self.get_database_info()
        if not info:
            return
        
        # 创建主信息面板
        main_info = Table.grid(padding=1)
        main_info.add_column("属性", style="cyan", no_wrap=True)
        main_info.add_column("值", style="white")
        
        main_info.add_row("数据库文件", self.db_path)
        main_info.add_row("文件大小", f"{info['file_size']:,} 字节")
        main_info.add_row("创建时间", info['created_time'].strftime("%Y-%m-%d %H:%M:%S"))
        main_info.add_row("修改时间", info['modified_time'].strftime("%Y-%m-%d %H:%M:%S"))
        main_info.add_row("表数量", str(len(info['tables'])))
        
        # 创建表信息表格
        if info['tables']:
            table_info = Table(title="数据库表信息")
            table_info.add_column("表名", style="cyan", no_wrap=True)
            table_info.add_column("行数", style="green", justify="right")
            
            for table_name, row_count in info['tables']:
                table_info.add_row(table_name, str(row_count))
        else:
            table_info = Text("暂无表", style="dim")
        
        # 显示信息
        console.print(Panel(
            main_info,
            title="[bold blue]数据库信息[/bold blue]",
            border_style="blue"
        ))
        
        if info['tables']:
            console.print(table_info)
        else:
            console.print(Panel(
                table_info,
                title="[bold yellow]表信息[/bold yellow]",
                border_style="yellow"
            ))

    def _reset_database(self):
        """[内部使用] 删除并重新创建数据库（谨慎操作）"""
        if self.is_database_exists():
            try:
                os.remove(self.db_path)
                console.print(f"[yellow]⚠️ 已删除数据库文件: {self.db_path}[/yellow]")
            except Exception as e:
                console.print(f"[red]✗ 删除数据库失败: {e}[/red]")
                return False

        return self.create_database()


def main():
    """主函数"""
    console.print("[bold blue]数据库管理系统 (SQLAlchemy)[/bold blue]", justify="center")
    console.print()
    
    db_manager = DatabaseManager()
    db_manager.display_database_info()
    db_manager._reset_database()  # 重置数据库（谨慎操作）

if __name__ == "__main__":
    main() 