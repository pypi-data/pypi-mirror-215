import inspect
import re
import shutil
import sys
from datetime import datetime
import logging
import os
import traceback
import zipfile
from pathlib import Path

from google.oauth2.service_account import Credentials

"""
To install libraries:
    pip install -r requirements.txt
"""
import google.cloud.logging
from google.cloud import error_reporting
from google.cloud.logging import Resource
from google.cloud.logging_v2.handlers import CloudLoggingHandler, setup_logging

"""
Check README.md for more information
"""

class Log:
    _LOGS_FOLER = "logs"

    _LOG_FILE_DATE_FORMAT = '%Y-%m-%d'
    _LOGS_DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S.%f'

    _PROJECT_NAME = os.path.basename(sys.path[1])

    class Level:
        INFO = "I"
        ERROR = "E"
        DEBUG = "D"
        WARNING = "W"

        @staticmethod
        def logger(level):
            if level == Log.Level.INFO:
                return logging.INFO
            if level == Log.Level.ERROR:
                return logging.ERROR
            if level == Log.Level.DEBUG:
                return logging.DEBUG
            if level == Log.Level.WARNING:
                return logging.WARNING
            return logging.NOTSET

    def __init__(self, log_name=None):
        self.log_name = log_name

        self._create_dirs()
        self._archive()
        self._generate_log_name()

        self.handler = logging.FileHandler(filename=os.path.join(self.log_dir, "any.log"), encoding='utf-8', mode='a+')
        logging.basicConfig(
            handlers=[
                self.handler
            ],
            format="%(asctime)s %(levelname)s: %(message)s",
            datefmt="%F %T",
            level=logging.NOTSET
        )
        self.logger = logging.getLogger(log_name)

        self.cloud_project_id = None

    def verbose(self, text, level):
        if level == self.Level.ERROR:
            text = f"{text}\n{traceback.format_exc()}"
        self.logger.log(self.Level.logger(level), text)
        if text:
            print(text)
        self._save_file(text, level)

    def info(self, text):
        self.verbose(text, self.Level.INFO)

    def warning(self, text):
        self.verbose(text, self.Level.WARNING)

    def debug(self, text):
        self.verbose(text, self.Level.DEBUG)

    def error(self, error):
        self.verbose(error, self.Level.ERROR)

    def setup_cloud_logging(self, project_id, credentials=None):
        self.cloud_project_id = project_id

        _resource = Resource(
            type="cloud_function",
            labels={
                "project_id": self.cloud_project_id,
                "function_name": self._PROJECT_NAME
            },
        )
        if credentials:
            client = google.cloud.logging.Client(
                project=self.cloud_project_id,
                credentials=Credentials.from_service_account_file(credentials)
            )
        else:
            client = google.cloud.logging.Client(project=self.cloud_project_id)
        setup_logging(self.handler)
        setup_logging(CloudLoggingHandler(client, resource=_resource))

    def _generate_log_name(self):
        _scripts = inspect.stack()
        _file_path = None
        for _script in _scripts:
            if _script.filename != __file__:
                _file_path = _script.filename
                break
        if _file_path:
            _filename_match = re.search(r"([^\\]+)\.py", _file_path)
            if _filename_match.lastindex > 0:
                self.log_name = _filename_match.group(_filename_match.lastindex)
        if not self.log_name:
            self.log_name = sys.argv[0]
        return self.log_name

    def _create_dirs(self):
        self.date = datetime.now().strftime(self._LOG_FILE_DATE_FORMAT)

        self.logs_dir = self._LOGS_FOLER
        self.log_dir = os.path.abspath(os.path.join(self.logs_dir, self.date))

        os.umask(0)
        os.makedirs(self.log_dir, exist_ok=True)

        self.log_file = os.path.join(self.log_dir, f"{self.log_name}.log")

        print(f"{self.log_name} logs can be found in {self.log_dir}")

    def _save_file(self, log, level):
        with open(self.log_file, "a+") as f:
            at = self._log_date()
            f.write(f"{at[:-3]} {level}: {log}\n")

    def _log_date(self):
        return datetime.now().strftime(self._LOG_FILE_DATE_FORMAT)

    def _archive(self):
        today = self._log_date()
        current_year = today[:4]
        log_directories = [
            os.path.join(self._LOGS_FOLER, directory)
            for directory in os.listdir(self._LOGS_FOLER)
            if os.path.isdir(os.path.join(self._LOGS_FOLER, directory))
            and directory != today
        ]

        zip_path = os.path.join(self._LOGS_FOLER, current_year + ".zip")
        zip_mode = "a" if os.path.exists(zip_path) else "w"
        with zipfile.ZipFile(zip_path, zip_mode, zipfile.ZIP_DEFLATED) as zip_file:
            for log_directory in log_directories:
                for file in os.listdir(log_directory):
                    if file.endswith(".log"):
                        file_path = os.path.join(log_directory, file)
                        zip_file.write(file_path, arcname=os.path.join(os.path.basename(log_directory), file))
                shutil.rmtree(log_directory)
