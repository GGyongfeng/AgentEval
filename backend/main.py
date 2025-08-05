import sys
from src.db import UserForm, QueryForm, EvaluationForm, FilesForm
from src.db.database import DatabaseManager


def main():
    #显示数据库信息
    db_manager = DatabaseManager()

    db_manager.display_database_info()

    user_form = UserForm()
    query_form = QueryForm()
    evaluation_form = EvaluationForm()
    files_form = FilesForm()


    #创建表
    query_form._create_tables()

    #添加query
    query_form.add_query(
        lazy_query="test",
        detail_query="test",
        creator_id=1,
        priority=1
    )

    #查询查询
    query = query_form.get_query_by_id(1)
    print(query)

    #显示表信息
    query_form.display_table_info()

if __name__ == "__main__":
    main()