import os
import subprocess
from django.core import management
from django.core.management.base import BaseCommand

SCRIPTS_FOLDER = "/app/scripts"
SCRIPTS_TO_RUN = [
    "init_manager.py",
    "init_skills.py",
    "init_projects.py",
    "init_task.py",
    "init_resource.py",
]

class Command(BaseCommand):
    help = """
    Init app:
    1. Run migrations
    2. Run custom scripts from /app/scripts/
    Usage: python src/manage.py initapp
    """

    def handle(self, *args, **kwargs):
        # Run migrations
        self.stdout.write(self.style.NOTICE("Running migrations..."))
        management.call_command("migrate", verbosity=2, interactive=False)

        # Run custom scripts
        for script in SCRIPTS_TO_RUN:
            script_path = os.path.join(SCRIPTS_FOLDER, script)
            self.stdout.write(self.style.NOTICE(f"Running {script_path}"))
            result = subprocess.run(["python", script_path])
            if result.returncode != 0:
                self.stdout.write(self.style.ERROR(f"Script {script} failed!"))
                break
        self.stdout.write(self.style.SUCCESS("Initialization complete."))
        