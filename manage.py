#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
# import dotenv

def get_environ():
    if os.environ.get("DJANGO_ENV") == 'local':
        print("ENVIRONMENT: local")
        print("USING DJANGO_SETTINGS_MODULE: quantumapp.dev_settings")
        print(os.environ.get("DJANGO_ENV"))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quantumapp.dev_settings')
    elif os.environ.get("DJANGO_ENV") == 'production':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quantumapp.settings')

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quantumapp.settings')
    # get_environ()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

# With DOTENV imported should look like this
# if __name__ == "__main__":
#     dotenv.read_dotenv()

#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)


# def main():
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quantumapp.settings')

#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)


# if __name__ == '__main__':
#     main()
