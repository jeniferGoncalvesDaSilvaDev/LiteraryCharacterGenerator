"""
Custom exceptions for the Multiverse Character Generator library.
"""


class MultiverseGeneratorError(Exception):
    """
    Base exception class for all Multiverse Character Generator errors.
    """
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
    
    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class InvalidUniverseError(MultiverseGeneratorError):
    """
    Raised when an invalid or unsupported universe is specified.
    """
    def __init__(self, message: str, universe: str = None, available_universes: list = None):
        self.universe = universe
        self.available_universes = available_universes or []
        
        if universe and available_universes:
            detailed_message = (
                f"{message}. Universe '{universe}' is not supported. "
                f"Available universes: {', '.join(available_universes)}"
            )
        else:
            detailed_message = message
        
        super().__init__(detailed_message, "INVALID_UNIVERSE")


class InvalidDetailsError(MultiverseGeneratorError):
    """
    Raised when character details don't match universe requirements.
    """
    def __init__(
        self,
        message: str,
        universe: str = None,
        expected_count: int = None,
        actual_count: int = None,
        required_fields: list = None
    ):
        self.universe = universe
        self.expected_count = expected_count
        self.actual_count = actual_count
        self.required_fields = required_fields or []
        
        if all([universe, expected_count is not None, actual_count is not None]):
            detailed_message = (
                f"{message}. Universe '{universe}' requires {expected_count} details, "
                f"but {actual_count} were provided."
            )
            if required_fields:
                detailed_message += f" Required fields: {', '.join(required_fields)}"
        else:
            detailed_message = message
        
        super().__init__(detailed_message, "INVALID_DETAILS")


class GenerationError(MultiverseGeneratorError):
    """
    Raised when character generation fails due to model or processing errors.
    """
    def __init__(self, message: str, cause: Exception = None):
        self.cause = cause
        
        if cause:
            detailed_message = f"{message}. Caused by: {str(cause)}"
        else:
            detailed_message = message
        
        super().__init__(detailed_message, "GENERATION_ERROR")


class ModelInitializationError(MultiverseGeneratorError):
    """
    Raised when model initialization fails.
    """
    def __init__(self, message: str, model_name: str = None, cause: Exception = None):
        self.model_name = model_name
        self.cause = cause
        
        if model_name:
            detailed_message = f"{message}. Failed to initialize model: {model_name}"
        else:
            detailed_message = message
        
        if cause:
            detailed_message += f". Caused by: {str(cause)}"
        
        super().__init__(detailed_message, "MODEL_INIT_ERROR")


class FileOperationError(MultiverseGeneratorError):
    """
    Raised when file operations (save/load) fail.
    """
    def __init__(self, message: str, filepath: str = None, operation: str = None, cause: Exception = None):
        self.filepath = filepath
        self.operation = operation
        self.cause = cause
        
        detailed_message = message
        if operation and filepath:
            detailed_message = f"{message}. Failed to {operation} file: {filepath}"
        elif filepath:
            detailed_message = f"{message}. File: {filepath}"
        
        if cause:
            detailed_message += f". Caused by: {str(cause)}"
        
        super().__init__(detailed_message, "FILE_OPERATION_ERROR")


class ValidationError(MultiverseGeneratorError):
    """
    Raised when input validation fails.
    """
    def __init__(self, message: str, field: str = None, value: str = None):
        self.field = field
        self.value = value
        
        if field:
            detailed_message = f"{message}. Invalid field: {field}"
            if value:
                detailed_message += f" (value: {value})"
        else:
            detailed_message = message
        
        super().__init__(detailed_message, "VALIDATION_ERROR")


class ConfigurationError(MultiverseGeneratorError):
    """
    Raised when configuration is invalid or missing.
    """
    def __init__(self, message: str, config_key: str = None, expected_type: str = None):
        self.config_key = config_key
        self.expected_type = expected_type
        
        detailed_message = message
        if config_key:
            detailed_message = f"{message}. Configuration key: {config_key}"
            if expected_type:
                detailed_message += f" (expected type: {expected_type})"
        
        super().__init__(detailed_message, "CONFIG_ERROR")


class ResourceError(MultiverseGeneratorError):
    """
    Raised when system resources are insufficient or unavailable.
    """
    def __init__(self, message: str, resource_type: str = None, required_amount: str = None):
        self.resource_type = resource_type
        self.required_amount = required_amount
        
        detailed_message = message
        if resource_type:
            detailed_message = f"{message}. Resource: {resource_type}"
            if required_amount:
                detailed_message += f" (required: {required_amount})"
        
        super().__init__(detailed_message, "RESOURCE_ERROR")
