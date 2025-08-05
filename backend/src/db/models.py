"""
共享数据库模型

数据库表关系图:
┌─────────────────┐       ┌─────────────────┐
│   user_form     │       │   query_form    │
│─────────────────│       │─────────────────│
│ id (PK)         │◄─────┐│ id (PK)         │
│ username        │      ││ lazy_query      │
│ password        │      ││ detail_query    │
│ nickname        │      ││ creator_id (FK) │───────┘
│ full_name       │      ││ priority        │
│ created_at      │      ││ created_at      │
│ updated_at      │      ││ updated_at      │
└─────────────────┘      │└─────────────────┘
        │                │         │
        │                │         ▼
        │                │┌─────────────────┐       ┌─────────────────┐
        │                ││ evaluation_form │       │   files_form    │
        │                ││─────────────────│       │─────────────────│
        └────────────────┼│ id (PK)         │◄──────│ id (PK)         │
                         ││ query_id (FK)   │       │ evaluation_id(FK)│
                         ││ agent           │       │ filename        │
                         ││ evaluator_id(FK)│───────┘│ content         │
                         ││ quality_score   │        │ file_type       │
                         ││ trajectory      │        │ file_size       │
                         ││ report_content  │        │ created_at      │
                         ││ created_at      │        │ updated_at      │
                         ││ updated_at      │        └─────────────────┘
                         │└─────────────────┘
                         │
                         └─────────────────────────────────────────────┘

关系说明:
1. user_form (用户表) 1:N query_form (查询表)
   - 一个用户可以创建多个查询
   - 外键: query_form.creator_id → user_form.id

2. user_form (用户表) 1:N evaluation_form (评估表)
   - 一个用户可以进行多个评估
   - 外键: evaluation_form.evaluator_id → user_form.id

3. query_form (查询表) 1:N evaluation_form (评估表)
   - 一个查询可以有多个评估
   - 外键: evaluation_form.query_id → query_form.id

4. evaluation_form (评估表) 1:N files_form (文件表)
   - 一个评估可以有多个相关文件
   - 外键: files_form.evaluation_id → evaluation_form.id

所有表的ORM模型都在这里定义，确保外键关系正确建立
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, LargeBinary, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# 创建共享模型实例
Base = declarative_base()

class UserModel(Base):
    """用户表单ORM模型"""
    __tablename__ = "user_form"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username = Column(String(50), unique=True, nullable=False, comment="用户名")
    password = Column(Text, nullable=False, comment="密码")
    nickname = Column(String(100), nullable=False, comment="昵称")
    full_name = Column(String(100), nullable=True, comment="全名")
    created_at = Column(String(50), nullable=False, comment="创建时间")
    updated_at = Column(String(50), nullable=True, comment="更新时间")

    # 关系定义
    created_queries = relationship("QueryModel", back_populates="creator")
    evaluations = relationship("EvaluationModel", back_populates="evaluator")

    def __repr__(self):
        return f"<UserModel(id={self.id}, username='{self.username}', nickname='{self.nickname}')>"

class QueryModel(Base):
    """查询表单ORM模型"""
    __tablename__ = 'query_form'
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment='查询ID')
    lazy_query = Column(Text, nullable=True, comment='简略query')
    detail_query = Column(Text, nullable=True, comment='详细query')
    creator_id = Column(Integer, ForeignKey('user_form.id'), nullable=True, comment='创建人ID')
    priority = Column(Integer, nullable=True, comment='优先级')
    created_at = Column(String(50), nullable=False, comment='创建时间')
    updated_at = Column(String(50), nullable=True, comment='更新时间')

    # 关系定义
    creator = relationship("UserModel", back_populates="created_queries")
    evaluations = relationship("EvaluationModel", back_populates="query")

    def __repr__(self):
        return f"<QueryModel(id={self.id}, creator_id={self.creator_id}, priority={self.priority})>"

class EvaluationModel(Base):
    """评估表单ORM模型"""
    __tablename__ = 'evaluation_form'
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment='评估ID')
    query_id = Column(Integer, ForeignKey('query_form.id'), nullable=False, comment='查询ID')
    agent = Column(String(100), nullable=True, comment='代理名称')
    evaluator_id = Column(Integer, ForeignKey('user_form.id'), nullable=True, comment='评估人ID')
    quality_score = Column(Integer, nullable=True, comment='质量分数')
    trajectory = Column(Text, nullable=True, comment='轨迹')
    report_content = Column(Text, nullable=True, comment='评估报告(Markdown格式)')
    created_at = Column(String(50), nullable=False, comment='创建时间')
    updated_at = Column(String(50), nullable=True, comment='更新时间')

    # 关系定义
    query = relationship("QueryModel", back_populates="evaluations")
    evaluator = relationship("UserModel", back_populates="evaluations")
    files = relationship("FilesModel", back_populates="evaluation")

    def __repr__(self):
        return f"<EvaluationModel(id={self.id}, query_id={self.query_id}, agent='{self.agent}')>"

class FilesModel(Base):
    """文件表单ORM模型"""
    __tablename__ = 'files_form'
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment='文件ID')
    evaluation_id = Column(Integer, ForeignKey('evaluation_form.id'), nullable=False, comment='评估ID')
    filename = Column(String(255), nullable=False, comment='文件名')
    content = Column(LargeBinary, nullable=True, comment='文件内容')
    file_type = Column(Enum("trajectory", "report", "deliverables", "pre_data", name="file_type_enum"), 
                      nullable=False, comment='文件类型')
    file_size = Column(Integer, nullable=True, comment='文件大小(字节)')
    created_at = Column(String(50), nullable=False, comment='创建时间')
    updated_at = Column(String(50), nullable=True, comment='更新时间')

    # 关系定义
    evaluation = relationship("EvaluationModel", back_populates="files")

    def __repr__(self):
        return f"<FilesModel(id={self.id}, evaluation_id={self.evaluation_id}, filename='{self.filename}')>"