class MouseAction:
    """Abstract base class for all mouse actions."""

    def execute(self) -> None:
        """Execute the mouse action. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement execute()")
