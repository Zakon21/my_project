from quart import Quart, jsonify, request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker, declarative_base,relationship
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
    address = Column(String(255), nullable = False)
    date = Column(TIMESTAMP, nullable = False)
    area = Column(Float, nullable = False)
    tariff = Column(Float, nullable = False)
    
class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key = True)
    title = Column(TEXT, nullable = False)
    date = Column(TIMESTAMP, nullable = False)
    image = Column(String(255), nullable = False)
    report = Column(BOOLEAN, nullable = False)
    txt = Column(TEXT, nullable = False)

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
        result = await session.execute(select(News))
        newses = result.scalars().all()
        newses_list = [
            {
                'id': news.id,
                'title': news.title,
                'date': news.date.strftime('%d.%m.%Y'),
                'image': news.image,
                'report': news.report,
                'txt': news.txt 
            }
            for news in newses
        ]
        return jsonify(newses_list)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)


