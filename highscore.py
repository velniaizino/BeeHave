from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///score.db')
Base = declarative_base()


class Score(Base):
    __tablename__ = 'Score'
    id = Column(Integer, primary_key=True)
    player_id = Column("Player ID", String)
    best = Column("Highscore", Integer)
    last = Column("Last Score", Integer)

    def __init__(self, player_id, player_best, player_last):
        self.player_id = player_id
        self.best = player_best
        self.last = player_last


Base.metadata.create_all(engine)
