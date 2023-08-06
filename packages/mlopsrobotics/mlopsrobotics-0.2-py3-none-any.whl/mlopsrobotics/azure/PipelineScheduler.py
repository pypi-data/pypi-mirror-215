from datetime import datetime
import argparse
from azure.ai.ml.entities import JobSchedule, RecurrenceTrigger, RecurrencePattern
from pytz import timezone
from azure.ai.ml.entities import Pipeline, Schedule
from utilities.logger_util import setup_logger
import loguru

# Set up Logger
setup_logger(True)
logger = loguru.logger


def create_pipeline_schedule(
    pipeline_instance: Pipeline,
    schedule_name: str,
    frequency: str,
    interval: int,
    start_time_hours: int,
    start_time_minutes: int,
    start_day: str,
) -> Schedule:
    """
    Creates a pipeline schedule for executing a pipeline instance at a specified frequency.

    Args:
        pipeline_instance (PipelineInstance): The pipeline instance to be executed.
        schedule_name (str): The name of the schedule.
        frequency (str): The frequency of the schedule (e.g., 'Minute', 'Hour', 'Day').
        interval (int): The interval between schedule occurrences.
        start_time_hours (int): The hour at which the schedule should start.
        start_time_minutes (int): The minute at which the schedule should start.

    Returns:
        JobSchedule: The created job schedule.

    Author: Anouk Okkema

    """

    logger.info("Creating pipeline schedule...")

    # Getting the current time in the Europe/Amsterdam timezone
    now_eur = datetime.now(timezone("Europe/Amsterdam")).replace(
        hour=start_time_hours, minute=start_time_minutes, second=0, microsecond=0
    )
    now_eur = now_eur.replace(tzinfo=None)

    schedule_start_time = datetime.utcnow()

    # Format the above DateTime using the strftime()
    logger.info("Current Time in Europe/Amsterdam TimeZone:", now_eur)

    # Define the recurrence trigger
    recurrence_trigger = RecurrenceTrigger(
        frequency=frequency,
        interval=interval,
        schedule=RecurrencePattern(
            hours=now_eur.hour, minutes=[now_eur.minute], week_days=[start_day]
        ),
        start_time=schedule_start_time,
        time_zone="W. Europe Standard Time",
    )

    logger.info("Recurrence trigger created.")

    # Create the job schedule
    job_schedule = JobSchedule(
        name=schedule_name, trigger=recurrence_trigger, create_job=pipeline_instance
    )

    logger.info("Job schedule created.")

    return job_schedule


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a schedule for a pipeline")
    parser.add_argument(
        "--pipeline_instance", required=True, help="the pipeline instance"
    )
    parser.add_argument("--schedule_name", required=True, help="Name for the schedule")
    parser.add_argument(
        "--frequency", default="Day", help="Frequency for the schedule (default: Day)"
    )
    parser.add_argument(
        "--interval", type=int, default=1, help="Interval for the schedule (default: 1)"
    )
    parser.add_argument(
        "--start_time_hours",
        type=int,
        default=10,
        help="Start time (hours) for the schedule (default: 10)",
    )
    parser.add_argument(
        "--start_time_minutes",
        nargs="+",
        type=int,
        default=[0, 1],
        help="Start time (minutes) for the schedule (default: 0 1)",
    )
    parser.add_argument(
        "--start_day",
        type=str,
        default="Monday",
        help="Start Day for the schedule (default: Monday)",
    )
    args = parser.parse_args()

    # Create pipeline schedule
    pipeline_schedule = create_pipeline_schedule(
        pipeline_instance=args.pipeline_instance,
        schedule_name=args.schedule_name,
        frequency=args.frequency,
        interval=args.interval,
        start_time_hours=args.start_time_hours,
        start_time_minutes=args.start_time_minutes,
        start_day=args.start_day,
    )
