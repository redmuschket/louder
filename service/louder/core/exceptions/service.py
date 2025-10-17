class ServiceError(Exception):
    """Base class for service-level errors."""
    pass

class ServiceDataError(ServiceError):
    """Error at the data service level"""
    pass


class ServiceRepositoryError(ServiceError):
    """Repository service level error"""
    pass


class ServiceStorageError(ServiceError):
    """Local storage service level error"""
    pass


class ServiceToolsError(ServiceError):
    """Error in auxiliary service"""
    pass