from enum import Enum

class ApiProtocol(Enum):
    DEFAULT = "rest"
    GRPC = "grpc"
    REST = "rest"