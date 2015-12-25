class SwaggerValidationError(Exception):
    """
    Raised when the Swagger spec is invalid.
    """
    pass

class MissingSpecError(Exception):
    """
    Raised when the swagger spec for a particular resource is not found.
    """
    pass
