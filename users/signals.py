# your_app_name/signals.py

from django.db.models.signals import pre_delete
from django.contrib.admin.models import LogEntry
from django.dispatch import receiver
from .models import CustomUser  # Ensure you import your CustomUser model

@receiver(pre_delete, sender=CustomUser)
def delete_related_admin_logs(sender, instance, **kwargs):
    LogEntry.objects.filter(user_id=instance.id).delete()
