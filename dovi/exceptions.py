class DoviError(Exception):
    """Base class for all dovi errors."""


class GenerationError(DoviError):
    """Raised when a document could not be generated."""


class ReplicationError(DoviError):
    """Raised when a source document could not be replicated."""


class BackendNotAvailableError(DoviError):
    """Raised when a render backend requires an optional dependency that is not installed."""

    def __init__(self, backend: str, extra: str) -> None:
        super().__init__(
            f"The '{backend}' backend requires optional dependencies. "
            f"Install them with: pip install 'dovi[{extra}]'"
        )
        self.backend = backend
        self.extra = extra
