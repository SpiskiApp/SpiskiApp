import csv
import logging
from datetime import datetime
from django.core.management.base import BaseCommand

from cage.models import List, ListItem, Prison


class Command(BaseCommand):
    help = "Import a list of detainees"

    def add_arguments(self, parser):
        parser.add_argument("--date", type=datetime.fromisoformat)
        parser.add_argument("--text", default="")
        parser.add_argument("--prison")
        parser.add_argument("--origin", required=True)

        parser.add_argument("--csv-delimiter", default=",")

        import_type = parser.add_mutually_exclusive_group(required=True)

        import_type.add_argument("--csv")
        # other import types...

    def handle(self, *args, **options):
        verbosity = int(options["verbosity"])
        logger = logging.getLogger("commands.import_list")
        logger.setLevel(verbosity)

        if options["prison"] is not None:
            prison = Prison.objects.get(name=options["prison"])
        else:
            prison = None
        list_ = List.objects.create(
            date=options["date"],
            prison=prison,
            text=options["text"],
            origin=options["origin"],
        )
        print("Created list", list_)

        if options["csv"] is not None:
            file_path = options["csv"]
            items = []

            with open(file_path) as fin:
                reader = csv.DictReader(fin, delimiter=options["csv_delimiter"])
                for record in reader:
                    print("Processing row", record)
                    items.append(
                        ListItem(
                            list=list_,
                            **record,
                        )
                    )

            ListItem.objects.bulk_create(items)
