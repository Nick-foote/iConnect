import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


logger = logging.getLogger('console-basic')
User = get_user_model()


class Command(BaseCommand):
    """Create SuperUser for start of project or when using AWS"""

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            logger.info("A temporary Admin User already set up in database")
        else:
            try:
                User.objects.create_superuser(
                    email= 'admin@gmail.com',
                    username = 'admin',
                    password = 'admin123'
                )
                logger.info("A temporary admin User has been created")
            except:
                logger.exception("Unable to create Admin user")
        