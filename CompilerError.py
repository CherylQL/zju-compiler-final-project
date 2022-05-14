class ParsingException(BaseException):

    def __init__(self, msg):
        self.msg = msg


class InTypeException(BaseException):

    def __init__(self, msg):
        self.msg = msg


class AnalysisException(BaseException):

    def __init__(self, msg):
        self.msg = msg


class DefMissingException(BaseException):

    def __init__(self, msg):
        self.msg = msg


class InLexException(BaseException):

    def __init__(self, msg):
        self.msg = msg


class MulDefException(BaseException):

    def __init__(self, msg):
        self.msg = msg


class OperationException(BaseException):

    def __init__(self, msg):
        self.msg = msg

