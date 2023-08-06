import os

from django.conf import settings
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Check manifest static files as if we were in production."

    def add_arguments(self, parser):
        parser.add_argument("--path", default="admin/css/base.css")

    def handle(self, *args, **options):
        """
        Test manifest static file storage locally against a specific file path.
        eg - python manage.py manifest_check admin/css/base.css
        """

        staticfiles_storages = [
            "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
            "whitenoise.storage.CompressedManifestStaticFilesStorage",
        ]

        # Defense against forgetfullness
        if settings.DEBUG:
            print("Ensure the following line is in settings")  # noqa
            print("     DEBUG = False")
            return

        if not any(x in settings.STATICFILES_STORAGE for x in staticfiles_storages):
            print("Ensure ONE of the following lines is in settings")  # noqa
            for storage in staticfiles_storages:
                print(f'    STATICFILES_STORAGE = "{storage}"')

        if not hasattr(settings, "STATIC_ROOT"):
            print("You need to set STATIC_ROOT")

        if not os.path.exists(settings.STATIC_ROOT):
            print("You need to run:")
            print("    python manage.py collectstatic")
            return

        # Ok, let's see...
        print(f"DEBUG: {settings.DEBUG}")
        print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
        url = ManifestStaticFilesStorage().url(options["path"], force=True)
        print(f'{options["path"]} => {url}')
