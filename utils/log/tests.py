from django.test import TestCase
from datetime import datetime
from pathlib import Path
from . logmixin import LogMixin
import contextlib
import os


DATA = datetime.today().strftime('%d/%m/%Y')
ROOT = Path(__file__).parent / 'log.txt'


class LogMixinTest(TestCase):
    def setUp(self) -> None:
        self.log = LogMixin()
        self.log.path = ROOT
        return super().setUp()

    def tearDown(self) -> None:
        with contextlib.suppress(OSError, FileNotFoundError):
            os.remove(ROOT)
        return super().tearDown()

    def test_should_write_log_error(self) -> None:
        msg = 'message error'
        self.log.log_error(msg)

        with open(ROOT, 'r') as file:
            read = file.read()
            self.assertIn('[LOG ERROR]', read)
            self.assertIn(DATA, read)
            self.assertIn(msg, read)

    def test_should_write_log_success(self) -> None:
        msg = 'message success'
        self.log.log_success(msg)

        with open(ROOT, 'r') as file:
            read = file.read()
            self.assertIn('[LOG SUCCESS]', read)
            self.assertIn(DATA, read)
            self.assertIn(msg, read)

    def test_must_keep_previous_data(self) -> None:
        """
            when writing new logs, the previous logs must be kept.
        """
        msg_error = 'message success'
        msg_success = 'message success'
        self.log.log_error(msg_error)
        self.log.log_success(msg_success)

        with open(ROOT, 'r') as file:
            read = file.read()
            self.assertIn(msg_error, read)
            self.assertIn(msg_success, read)
