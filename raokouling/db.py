# -*- encoding: utf-8 -*-

import hashlib
import time
from sqlalchemy import create_engine
from sqlalchemy import Column, VARCHAR, Integer, TIMESTAMP, CHAR, TEXT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://root:12345678@localhost/my_test?charset=utf8')
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()


class YoududuanziItem(Base):
    """段子信息"""
    __tablename__ = 'raokouling'
    desc = '绕口令信息'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    duplicate_hash = Column(CHAR(40), index=True, unique=True, doc={'zh': "url hash"})
    crawl_time = Column(TIMESTAMP, doc={'zh': '当前时间'})
    key_word = Column(VARCHAR(20), doc={'zh': '关键词'})
    detail_title = Column(VARCHAR(200), doc={'zh': '绕口令标题'})
    detail_url = Column(VARCHAR(200), index=True, doc={'zh': '绕口令的url'})
    content_html = Column(TEXT, doc={'zh': '绕口令内容'})
    content = Column(TEXT, doc={'zh': '绕口令内容'})

    @classmethod
    def creat_table(cls):
        """创建数据表"""
        cls.__table__.create(bind=engine, checkfirst=True)

    def insert(self, key_word, detail_title, detail_url, content_html, content):
        url_sha = self.get_contern_url_hash(content)
        crawled_time = time.strftime('%Y-%m-%d %H:%M:%S')
        try:
            is_exist = session.query(YoududuanziItem).filter(YoududuanziItem.duplicate_hash == url_sha).all()
            if not is_exist:
                item = YoududuanziItem(duplicate_hash=url_sha,
                                       crawl_time=crawled_time,
                                       key_word=key_word,
                                       detail_title=detail_title,
                                       detail_url=detail_url,
                                       content_html=content_html,
                                       content=content)
                session.add(item)
                session.commit()
                return True
            else:
                return False
        except BaseException as e:
            session.rollback()
            session.close()
            raise BaseException(f"数据插入失败: \n{url_sha} \n{detail_url} \n{e}")

    def get_contern_url_hash(self, content_url):
        hash = hashlib.sha1()
        hash.update(str(content_url).encode('utf-8'))
        url_sha = hash.hexdigest()
        return url_sha