# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

"""main scheduler file."""
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler

import scheduler.inactivity_courses as inactivity
import scheduler.deadlineManager as deadline_manager


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

        :param course_id: course to check the deadlines for
        """
        job = self.add_job(deadline_manager.notify_about_passed_deadlines, args=[course_id])
        self.jobs[str(course_id) + "late"] = job

    def add_deadline_early_notification(self, course_id, time_before):
        """
        Add scheduler job to send notifications for upcoming deadlines at 3 AM.

        :param course_id: course to check the deadlines for
        :param time_before: time in seconds the user should be warned in advance
        """
        job = self.add_job(deadline_manager.notify_about_upcoming_deadlines, args=[time_before, course_id])
        self.jobs[str(course_id) + "early"] = job

    def add_inactivity_notification(self, course_id, inactivity_time):
        """
        Add scheduler job to send notifications for inactivity of students at 3 AM.

        :param course_id: course to check the deadlines for
        :param inactivity_time: number of days the activity needs to be checked for, default is 7 days
        """
        inactivity_manager = inactivity.create_job
        job = self.add_job(inactivity_manager, [course_id, inactivity_time])
        self.jobs[str(course_id) + "inactive"] = job

    def add_job(self, function, args=None):
        """
        Add a cron job to the scheduler.

        :param function: the function that needs to be performed by the cron job
        :param args: arguments that are needed to be send with the function
        :return: the job that is created
        """
        job = self.scheduler.add_job(function, 'cron', hour='3', minute='0', args=args)
        return job

    def remove_job(self, course_id, job_type):
        """
        Remove a scheduled job.

        :param course_id: the course id
        :param job_type: the type of job for the course. Can be 'late', 'early' or 'inactive'
        """
        self.jobs[str(course_id) + job_type].remove()
        del self.jobs[str(course_id) + job_type]


main_scheduler = SchedulerConfig()
