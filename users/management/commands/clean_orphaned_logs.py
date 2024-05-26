# your_app/management/commands/clean_orphaned_logs.py

from django.core.management.base import BaseCommand
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Clean up orphaned admin log entries'

    def handle(self, *args, **kwargs):
        orphaned_logs = LogEntry.objects.exclude(user_id__in=User.objects.values('id'))
        orphaned_logs_count = orphaned_logs.count()
        orphaned_logs.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {orphaned_logs_count} orphaned log entries.'))
