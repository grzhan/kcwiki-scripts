import schedule
import click
import time
import traceback
from .fetch import fetch_start2_ooi
from ..common.utils import Echo as echo
from lib.services.subtitle import SubtitleService


@click.group()
def plan_cmd():
    pass


@plan_cmd.command(name='plan')
@click.pass_context
def plan(ctx):
    """job scheduling"""
    schedule.every().hour.do(fetch_start2_ooi)
    schedule.every().day.at('05:00').do(task_update_subtitle)
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                echo.warn('aborted.')
                return
            traceback.print_exc()
        time.sleep(5)


def task_update_subtitle():
    service = SubtitleService
    service.deploy()

