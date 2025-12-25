#!/usr/bin/env python3
# 
# datetime_manager.py
#
# [概要]
#
#
#
#
#
#

from datetimejp import JDatetime

from datetime import datetime, timedelta
from logging import getLogger

# 専用のロガーを作成
logger = getLogger(__name__)


class DateTimeManager:
    def __init__(self):
        self.today = JDatetime.today()
