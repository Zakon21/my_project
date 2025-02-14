from quart import Quart, jsonify, request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, DateTime, TIMESTAMP, TEXT, BOOLEAN, ForeignKey
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

app = Quart(__name__)
Base = declarative_base()

engine: AsyncEngine = create_async_engine(os.getenv('DATABASE_URL'), echo = True)

async_session = sessionmaker(
    engine,
    class_ = AsyncSession,
    expire_on_commit = False,
)

class House(Base):
    __tablename__ = 'houses'
    id = Column(Integer, primary_key = True)
    address = Column(String, nullable = False)
    date = Column(TIMESTAMP, nullable = False)
    area = Column(Float, nullable = False)
    tariff = Column(Float, nullable = False)
    house_id = Column(Integer, nullable = False)

    contracts = relationship('Contract', back_populates = 'house')
    protocols = relationship('Protocol', back_populates = 'house')
    documents = relationship('Document', back_populates = 'house')
    
class New(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key = True)
    title = Column(TEXT, nullable = False)
    date = Column(TIMESTAMP, nullable = False)
    image = Column(String, nullable = False)
    report = Column(BOOLEAN, nullable = False)
    txt = Column(TEXT, nullable = False)
    report_id = Column(Integer, nullable = False)

class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key = True)
    txt = Column(TEXT, nullable = False)
    image = Column(String, nullable = False)
    report_id = Column(Integer, nullable = False) 

class Contract(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key = True, nullable = False)
    txt = Column(TEXT, nullable = False)
    house_id = Column(Integer, ForeignKey('houses.id', ondelete = 'CASCADE'), nullable = False)

    house = relationship('House', back_populates = 'contracts')
class Protocol(Base):
    __tablename__ = 'protocols'
    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String, nullable = False)
    number = Column(Integer, nullable = False)
    date = Column(TIMESTAMP, nullable = False)
    link = Column(String, nullable = False)
    house_id = Column(Integer, ForeignKey('houses.id', ondelete = 'CASCADE'), nullable = False)

    house = relationship('House', back_populates = 'protocols')
class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String, nullable = False)
    number = Column(Integer, nullable = False)
    date = Column(TIMESTAMP, nullable = False)
    link = Column(String, nullable = False)
    house_id = Column(Integer, ForeignKey('houses.id', ondelete = 'CASCADE'), nullable = False)

    house = relationship('House', back_populates = 'documents')

@app.route('/houses', methods = ['GET'])
async def get_houses():
    async with async_session() as session:
        result = await session.execute(select(House).order_by(House.date.desc()))
        houses = result.scalars().all()
        houses_list = [
        {
            'id': house.id,
            'address': house.address,
            'date': house.date.strftime('%d.%m.%Y'),
            'area': f'{house.area:.2f}',
            'tariff': f'{house.tariff:.2f}'
        }
        for house in houses
    ]
    return jsonify(houses_list)

@app.route('/news', methods = ['GET'])
async def get_news():
    async with async_session() as session:
        result = await session.execute(select(New).order_by(New.date.desc()))
        news = result.scalars().all()
        news_list = [
            {
                'id': new.id,
                'title': new.title,
                'date': new.date.strftime('%d.%m.%Y'),
                'image': new.image,
                'report': new.report,
                'txt': new.txt 
            }
            for new in news
        ]
        return jsonify(news_list)

@app.route('/contracts', methods = ['GET'])
async def get_contracts():
    async with async_session() as session:
        result = await session.execute(select(Contract))
        contracts = result.scalars().all()
        contracts_list = [
            {
                'id': contract.id,
                'txt': contract.txt,
                'house_id': contract.house_id
            }
            for contract in contracts
        ]
        return jsonify(contracts_list)
    
@app.route('/protocols', methods = ['GET'])
async def get_protocols():
    async with async_session() as session:
        result = await session.execute(select(Protocol))
        protocols = result.scalars().all()
        protocols_list = [
            {
                'id': protocol.id,
                'name': protocol.name,
                'number': protocol.number,
                'date': protocol.date.strftime('%d.%m.%Y'),
                'house_id': protocol.house_id,
                'link': protocol.link
            }
            for protocol in protocols
        ]
        return jsonify(protocols_list)

@app.route('/documents', methods = ['GET'])
async def get_documents():
    async with async_session() as session:
        result = await session.execute(select(Document))
        documents = result.scalars().all()
        documents_list = [
            {
                'id': document.id,
                'name': document.name,
                'number': document.number,
                'date': document.date.strftime('%d.%m.%Y'),
                'link': document.link,
                'house_id': document.house_id
            }
            for document in documents
        ]
        return jsonify(documents_list)

@app.route('/reports', methods = ['GET'])
async def get_reports():
    async with async_session() as session:
        result = await session.execute(select(Report))
        reports = result.scalars().all()
        reports_list = [
            {
                'id': report.id,
                'txt': report.txt,
                'image': report.image,
                'report_id': report.report_id
            }
            for report in reports
        ]
        return jsonify(reports_list)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)


