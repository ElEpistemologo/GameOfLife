class WebSocketSession (object):

    def __init__(self, session_id, websocket):
        self.session_id = session_id
        self.__websocket = websocket

    @property
    def session_id(self):
        return self.__session_id

    @session_id.setter
    def session_id(self, session_id):
        self.__session_id = session_id