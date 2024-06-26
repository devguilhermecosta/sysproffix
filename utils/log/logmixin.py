from pathlib import Path
from datetime import datetime


ROOT = Path(__file__).parent.parent.parent / 'log.txt'
FORMATED_DATA = datetime.today().strftime('%d/%m/%Y - %H:%M:%S')


class LogMixin:
    path = ROOT

    def __cursor(self, content: str) -> None:
        with open(self.path, 'a+') as file:
            file.write(content)

    def log_error(self, content: str) -> None:
        self.__cursor(
            f'[LOG ERROR] - {FORMATED_DATA} - {content}\n'  # noqa: E501
        )

    def log_success(self, content: str) -> None:
        self.__cursor(
            f'[LOG SUCCESS] - {FORMATED_DATA} - {content}\n'  # noqa: E501
        )
