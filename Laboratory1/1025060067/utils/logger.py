class Logger:
    """
    A simple in-memory logger to record system events and notification attempts.
    """
    _logs = []

    @classmethod
    def log(cls, message: str):
        """
        Logs a message to the in-memory log list.
        """
        cls._logs.append(message)
        print(f"LOG: {message}") # Also print to console for visibility

    @classmethod
    def get_logs(cls) -> list[str]:
        """
        Retrieves all recorded logs.
        """
        return list(cls._logs)

    @classmethod
    def clear_logs(cls):
        """
        Clears all recorded logs.
        """
        cls._logs = []
