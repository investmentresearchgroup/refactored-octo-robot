import csv
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.core.exceptions import FieldError
from tracker.loader import FIELDS


def fields_validated(csv_fields, model_fields):
    """Method to check if csv headers contain model required fields"""
    return all(x in csv_fields for x in model_fields)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-f', '--filename',
                            help="loader csv file", type=str)
        parser.add_argument(
            '-m', '--model', help="Implemented Data Model. See FIELDS.keys()")

    def handle(self, *args, **options):
        if options['model'] not in FIELDS.keys():
            raise FieldError(
                f'Model not found!: Existing models are {FIELDS.keys()}')

        model = FIELDS[options['model']]
        object_method, model_fields = model['method'], model['required_fields']

        with open(options['filename'], 'r') as csv_file:
            csv_ = csv.DictReader(csv_file)

            if fields_validated(csv_.fieldnames, model_fields):
                for line in csv_:
                    try:
                        created_object, created = object_method(line)
                        if created:
                            self.stdout.write(self.style.SUCCESS(
                                f"Created {created_object} successfully!"))
                        else:
                            self.stdout.write(self.style.WARNING(
                                f"{created_object} was not created possibly due to an IntegrityError!"))
                    except (ValueError, IntegrityError) as e:
                        self.stdout.write(self.style.WARNING(
                            f"{created_object} object was skipped with the following message: {e}"))
            else:
                raise FieldError(
                    f'Model: {options["model"]} requires the following fields: {model_fields}.')
