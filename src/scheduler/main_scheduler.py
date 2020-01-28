# This program has been developed by students from the bachelor Computer Science at Utrecht University within the
# Software and Game project course
# ©Copyright Utrecht University Department of Information and Computing Sciences.
"""Main scheduler file."""
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler

import scheduler.inactivity_courses as inactivity
import scheduler.deadline_manager as deadline_manager


class SchedulerConfig:
    """Start the scheduler and add notification jobs for 3 AM."""

    name = 'scheduler'

    def __init__(self):
        """Instantiate the scheduler and add jobs."""
        self.jobs = {}
        self.scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
        self.scheduler.start()

    def add_deadline_late_notification(self, course_id):
        """
        Add scheduler job to send notifications for missed deadlines at 3 AM.

        :param course_id: Course to check the deadlines for.
        :type course_id: int
        """
        self.add_cron_job(deadline_manager.notify_about_passed_deadlines, str(course_id) + "late", args=[course_id])

    def add_deadline_early_notification(self, course_id, time_before):
        """
        Add scheduler job to send notifications for upcoming deadlines at 3 AM.

        :param course_id: Course to check the deadlines for.
        :type course_id: int
        :param time_before: Time in seconds the user should be warned in advance.
        :type time_before: int
        """
        self.add_cron_job(
            deadline_manager.notify_about_upcoming_deadlines,
            str(course_id) + "early", args=[time_before, course_id])

    def add_inactivity_notification(self, course_id, inactivity_time):
        """
        Add scheduler job to send notifications for inactivity of students at 3 AM.

        :param course_id: Course to check the deadlines for.
        :type course_id: int
        :param inactivity_time: Number of days the activity needs to be checked for, default is 7 days.
        :type inactivity_time: int
        """
        inactivity_manager = inactivity.create_job
        self.add_cron_job(inactivity_manager, str(course_id) + "inactive", [course_id, inactivity_time])

    def add_cron_job(self, function, job_name, args=None):
        """
        Add a cron job to the scheduler.

        :param function: The function that needs to be performed by the cron job.
        :type: function or str
        :param args: Arguments that are needed to be send with the function.
        :type args: all types
        :return: The job that is created.
        :rtype: job
        """
        job = self.scheduler.add_job(function, args=args, trigger='cron', hour='3', minute='0')
        self.jobs[job_name] = job
        job = self.scheduler.add_job(function, 'cron', hour='3', minute='0', args=args)
        return job

    def remove_job(self, course_id, job_type):
        """
        Remove a scheduled job.

        :param course_id: The course id.
        :type course_id: int
        :param job_type: The type of job for the course. Can be 'late', 'early' or 'inactive'.
        :type job_type: str
        """
        self.jobs[str(course_id) + job_type].remove()
        del self.jobs[str(course_id) + job_type]


main_scheduler = SchedulerConfig()
