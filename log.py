import logging
import logging.handlers

class Logger(object):
    __object = None 
    def __new__(cls):       # 单例模式
        if not cls.__object:
            cls.__object = super().__new__(cls)
        return cls.__object

    def __init__(self, name='root'):
        self.__logger = logging.getLogger(name)
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(filename)s(line:%(lineno)d) : %(message)s', '%Y-%m-%d %H:%M:%S')

        handler_info = logging.handlers.TimedRotatingFileHandler('logs/info.log', when='D', interval=1) # 每 when * interval 生成一个日志文件
        handler_warn = logging.handlers.TimedRotatingFileHandler('logs/warning.log', when='D', interval=1)
        handler_err = logging.handlers.TimedRotatingFileHandler('logs/error.log', when='D', interval=1)

        handler_info.setFormatter(formatter)
        handler_warn.setFormatter(formatter)
        handler_err.setFormatter(formatter)

        handler_info.setLevel(logging.INFO)
        handler_warn.setLevel(logging.WARNING)
        handler_err.setLevel(logging.ERROR)

        self.__logger.addHandler(handler_info)
        self.__logger.addHandler(handler_warn)
        self.__logger.addHandler(handler_err)

        self.__logger.setLevel(logging.INFO) # 设置默认 为 info 级别

    def get_logger(self):
        return self.__logger