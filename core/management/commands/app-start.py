from django.core.management.commands.startapp import Command as StartAppCommand


class Command(StartAppCommand):
    help = "Custom command to create a Django app with additional options."

    def handle(self, *args, **options):
        # Call the original startapp command to perform the initial app creation
        super().handle(*args, **options)

        # Add your custom logic here
        app_name = args[0]
        self.stdout.write(
            f"App '{app_name}' created successfully with custom features!")

        # Example of custom logic: Create additional files
        self.create_custom_files(app_name)

    def create_custom_files(self, app_name):
        # Logic to create additional files in the new app directory
        app_dir = f'{app_name}/'
        additional_dirs = {
            "serializers": {
            },
            "permissions": {
            }
        }
        additional_files = ['serializers.py', 'permissions.py']

        for file in additional_files:
            with open(f'{app_dir}{file}', 'w') as f:
                f.write(f'# {file} for {app_name}\n')
            self.stdout.write(f"Created {file} in {app_dir}")
