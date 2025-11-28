# messages/management/commands/create_sample_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample users for testing'

    def handle(self, *args, **kwargs):
        usernames = ['alice', 'bob', 'charlie', 'dave', 'eve']
        created_count = 0

        for username in usernames:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'password': 'testpass123',  # this will store as raw, we will set_password after
                }
            )
            if created:
                user.set_password('testpass123')  # hash the password properly
                user.save()
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Created {created_count} users.'))
