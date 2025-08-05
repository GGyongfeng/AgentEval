"""
测试所有表单的基本功能

这个文件用于测试 user_form, query_form, evaluation_form, files_form 的基本增删查改操作
"""

from src.db.Forms.user_form import UserForm
from src.db.Forms.query_form import QueryForm
from src.db.Forms.evaluation_form import EvaluationForm
from src.db.Forms.files_form import FilesForm
from src.db.database import DatabaseManager
from rich.console import Console

console = Console()

def test_user_form():
    """测试用户表单功能"""
    console.print("\n[bold blue]=== 测试用户表单 ===[/bold blue]")
    
    user_form = UserForm("test.db")
    
    # 测试添加用户
    console.print("\n[green]1. 添加用户测试[/green]")
    user_form.add_user("testuser1", "password123", "测试用户1", "测试用户全名1")
    user_form.add_user("testuser2", "password456", "测试用户2", "测试用户全名2")
    
    # 测试查询用户
    console.print("\n[green]2. 查询用户测试[/green]")
    user = user_form.get_user_by_username("testuser1")
    if user:
        console.print(f"找到用户: {user.username} - {user.nickname}")
    
    # 测试更新用户
    console.print("\n[green]3. 更新用户测试[/green]")
    user_form.update_user("testuser1", nickname="更新后的昵称")
    
    # 显示所有用户
    console.print("\n[green]4. 显示所有用户[/green]")
    user_form.display_UserForm()

def test_query_form():
    """测试查询表单功能"""
    console.print("\n[bold blue]=== 测试查询表单 ===[/bold blue]")
    
    query_form = QueryForm("test.db")
    
    # 测试添加查询
    console.print("\n[green]1. 添加查询测试[/green]")
    query_form.add_query(
        lazy_query="简单的查询",
        detail_query="这是一个详细的查询描述",
        creator_id=1,
        priority=1
    )
    query_form.add_query(
        lazy_query="另一个查询",
        detail_query="另一个详细的查询描述",
        creator_id=1,
        priority=2
    )
    
    # 测试查询查询
    console.print("\n[green]2. 查询测试[/green]")
    query = query_form.get_query_by_id(1)
    if query:
        console.print(f"找到查询: ID={query.id}, 详细查询={query.detail_query}")
    
    # 测试更新查询
    console.print("\n[green]3. 更新查询测试[/green]")
    query_form.update_query(1, priority=5)
    
    # 显示所有查询
    console.print("\n[green]4. 显示所有查询[/green]")
    query_form.display_queries()

def test_evaluation_form():
    """测试评估表单功能"""
    console.print("\n[bold blue]=== 测试评估表单 ===[/bold blue]")
    
    evaluation_form = EvaluationForm("test.db")
    
    # 测试添加评估
    console.print("\n[green]1. 添加评估测试[/green]")
    evaluation_form.add_evaluation(
        query_id=1,
        agent="测试代理",
        evaluator_id=1,
        quality_score=85,
        trajectory="这是轨迹数据",
        report_content="这是评估报告内容"
    )
    evaluation_form.add_evaluation(
        query_id=2,
        agent="另一个代理",
        evaluator_id=1,
        quality_score=90,
        trajectory="另一个轨迹数据",
        report_content="另一个评估报告内容"
    )
    
    # 测试查询评估
    console.print("\n[green]2. 查询评估测试[/green]")
    evaluation = evaluation_form.get_evaluation_by_id(1)
    if evaluation:
        console.print(f"找到评估: ID={evaluation.id}, 代理={evaluation.agent}")
    
    # 测试更新评估
    console.print("\n[green]3. 更新评估测试[/green]")
    evaluation_form.update_evaluation(1, quality_score=95)
    
    # 显示所有评估
    console.print("\n[green]4. 显示所有评估[/green]")
    evaluation_form.display_evaluations()

def test_files_form():
    """测试文件表单功能"""
    console.print("\n[bold blue]=== 测试文件表单 ===[/bold blue]")
    
    files_form = FilesForm("test.db")
    
    # 测试添加文件
    console.print("\n[green]1. 添加文件测试[/green]")
    files_form.add_file(
        evaluation_id=1,
        filename="test_trajectory.json",
        file_type="trajectory",
        content=b"trajectory file content",
        file_size=1024
    )
    files_form.add_file(
        evaluation_id=1,
        filename="test_report.md",
        file_type="report",
        content=b"report file content",
        file_size=2048
    )
    
    # 测试查询文件
    console.print("\n[green]2. 查询文件测试[/green]")
    file_record = files_form.get_file_by_id(1)
    if file_record:
        console.print(f"找到文件: ID={file_record.id}, 文件名={file_record.filename}")
    
    # 测试更新文件
    console.print("\n[green]3. 更新文件测试[/green]")
    files_form.update_file(1, file_size=1500)
    
    # 显示所有文件
    console.print("\n[green]4. 显示所有文件[/green]")
    files_form.display_files()

def main():
    """主测试函数"""
    console.print("[bold yellow]开始测试所有表单功能[/bold yellow]")
    
    try:
        # 测试用户表单
        test_user_form()
        
        # 测试查询表单
        test_query_form()
        
        # 测试评估表单
        test_evaluation_form()
        
        # 测试文件表单
        test_files_form()
        
        console.print("\n[bold green]✓ 所有测试完成！[/bold green]")
        
    except Exception as e:
        console.print(f"\n[bold red]✗ 测试过程中出现错误: {e}[/bold red]")

if __name__ == "__main__":
    main() 