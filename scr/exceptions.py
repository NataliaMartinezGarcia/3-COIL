# Common exceptions used in open_files and model_handler

class FileNotSelectedError(Exception):
    """Exception for non selected files."""
    pass

class FileFormatError(Exception):
    """Exception for invalid file formats."""
    pass

class EmptyDataError(Exception):
    """Exception for empty files or non-existent tables."""
    pass