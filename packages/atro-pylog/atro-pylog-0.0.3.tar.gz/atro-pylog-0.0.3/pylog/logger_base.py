from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def debug(self, message: str):
        pass

    @abstractmethod
    def info(self, message: str):
        print("here")
        pass

    @abstractmethod
    def warning(self, message: str):
        pass

    @abstractmethod
    def error(self, message: str):
        pass

    @abstractmethod
    def critical(self, message: str):
        pass

    @abstractmethod
    def shutdown(self):
        pass

    @abstractmethod
    def level(self, level: str):
        pass

    def catch(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.error(f'Error occurred in function {func.__name__} Error: {str(e)}, Args: {args}, Kwargs: {kwargs}')
                raise e  # Re-throwing the exception so that the error can be handled upstream if needed
        return wrapper    