import logging


class LoggingHandler(logging.Handler):

    def __init__(self, text_widget) -> None:
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record) -> None:
        """Ecrit le message dans le widget text_widget"""
        msg = self.format(record)
        self.text_widget.insert('end', f'{msg}\n')
