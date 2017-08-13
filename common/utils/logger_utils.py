import uuid


class LoggerUtils:
    def getTraceId(self):
        return str(uuid.uuid1())
