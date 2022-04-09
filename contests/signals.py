from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Announcement, Registration
from notifications.signals import notify

@receiver(post_save, sender=Announcement)
def create_notification(sender, instance, created, **kwargs):
    print(sender)
    print(instance)
    print(created)
    if created:
        announcement = instance
        registrations = Registration.objects.filter(contest_id=announcement.contest.id)
        for registration in registrations:
            user_objects = User.objects.filter(id=registration.user_id)
            if user_objects.count() > 0:
                user = user_objects[0]
                notify.send(sender=user, recipient=user, verb='new contest announcement')
