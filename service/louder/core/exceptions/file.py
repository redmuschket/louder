class FileError(Exception):
    """General error"""
    pass

class FileCreationError(FileError):
    """Error when creating a file in the system."""
    pass

class FileGetError(FileError):
    """Error when creating a file in the system."""
    pass

class FileEditError(FileError):
    """Error when editing a file in the system."""
    pass