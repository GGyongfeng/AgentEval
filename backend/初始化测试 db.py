import os

from rich.console import Console

from src.db import UserForm, QueryForm, EvaluationForm, FilesForm, DatabaseManager

console = Console()

db = DatabaseManager()
user_form = UserForm()
query_form = QueryForm()
evaluation_form = EvaluationForm()
files_form = FilesForm()



def add_user():
    if user_form.get_user_by_username("admin") is None:
        user_form.add_user(
            username="admin", 
            password="123456", 
            nickname="admin", 
            full_name="admin"
        )
    else:
        console.print("[bold red]用户admin已存在[/bold red]")

    if user_form.get_user_by_username("user1") is None:
        user_form.add_user(
            username="user1", 
            password="123456", 
            nickname="user1", 
            full_name="user1"
        )
    else:
        console.print("[bold red]用户user1已存在[/bold red]")

def batch_add_queries(query_form: QueryForm, user_form: UserForm, folder_path: str, priority: int = 1, username: str = "admin"):
    """批量导入 query 文本到数据库"""
    user = user_form.get_user_by_username(username)
    if not user:
        print(f"用户 {username} 不存在")
        return

    for i in range(1, 26):
        filename = f"query-{i}.txt"
        file_path = os.path.join(folder_path, filename)

        if not os.path.exists(file_path):
            print(f"[跳过] 未找到文件: {file_path}")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            print(f"[跳过] 文件内容为空: {filename}")
            continue

        success = query_form.add_query(
            detail_query=content,
            creator_id=user.id,
            priority=priority
        )

        if success:
            print(f"[✓] 成功导入: {filename}")
        else:
            print(f"[✗] 导入失败: {filename}")

def reset():
    db._reset_database()
    user_form._create_tables()
    add_user()
    batch_add_queries(query_form, user_form, "/Users/guyongfeng/Desktop/Sophiapro/benchmark/querys/高优_25 条query", 1, "admin")
    db.display_database_info()


def main():
    """主函数"""
    console.print(
        "[bold blue]数据库管理系统 (SQLAlchemy)[/bold blue]", justify="center"
    )
    console.print()

    # reset()
    # db.display_database_info()
    # evaluation_form.display_table_info()
    # evaluation_form.display_lines()
    # evaluation_form.display_structure()






if __name__ == "__main__":
    main()
