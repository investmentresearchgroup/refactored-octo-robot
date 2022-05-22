import loaders
from csv import DictReader
from django.core.management import BaseCommand
from typing import Optional, Any
from django.core.exceptions import ValidationError

SUPPORTED_LOADERS = {"advisor", "client", "account", "security", "trx", "price"}


def is_supported_loader(ldr: str) -> bool:
    return ldr in SUPPORTED_LOADERS

def process_row_by_row():
    ...


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "-f", "--file", help="full path to csv loader file", type=str
        )

        parser.add_argument("-m", "--model", help="Implemented model")

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        file, method = options["file"], options["model"]

        if not is_supported_loader(method):
            raise ValidationError(f"Indicated method : '{method}' is not supported!")

        ldr = getattr(loaders, method)

        with open(file, "r") as csv_file:
            csv_ = DictReader(csv_file)
            if method == "price":
                self.stdout.write(
                    "Creating prices...."
                )
                ldr(csv_)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created {method} objects!"
                    )
                )
            else:
                for row in csv_:
                    try:
                        ldr(row)
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Successfully created {method} object for {row}!"
                            )
                        )
                    except Exception as exp:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Got the following exception while processing row {row}: {exp}"
                            )
                        )
        self.stdout.write(self.style.SUCCESS(f"Successfully loaded {method} data!"))
