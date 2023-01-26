from trade.spot import submit_order
from telegram.Client.message import broadcast_messages
from crud.recommendation import recommendation as crudRecommendation
from db.session import SessionLocal
from models.recommendation import Recommendation

session = SessionLocal()

class Strategy:
    def __init__(self, asset: str, timeframe: str, watchlist_id: int):
        self.asset = asset
        self.timeframe = timeframe
        self.watchlist_id = watchlist_id

    def get_last(self) -> Recommendation:
        recom = crudRecommendation.get_last(db=session, watchlist_id=self.watchlist_id)
        return recom

    def insert_database(self, position: str, current_price: float, risk: str):
        pass

    def broadcast(self, position: str, current_price: float, risk: str):
        pass

    def buy(self):
        pass

    def sell(self):
        pass

    def logic(self, row):
        raise Exception("NotImplementedException")

    def signal(self):
        """
            check last row of processed dataframe to generate signal
        """
        last_row_detector = self.get_recommendations().tail(1)
        position = last_row_detector['recommendation'].values[0]
        if self.last_position != position and position is not None:
            close = float(last_row_detector['close'].values[0])

            self.broadcast(position=position, current_price=close, risk=last_row_detector['risk'].values[0])
            self.insert_database(position=position, current_price=close,
                                 risk=last_row_detector['risk'].values[0])
            self.order(position=position)

