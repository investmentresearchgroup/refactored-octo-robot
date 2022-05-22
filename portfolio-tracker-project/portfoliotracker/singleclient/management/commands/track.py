from django.core.management import BaseCommand
from analytics.tracking import TrackingModel
from util import TrackingUtils
from loaders import position
from typing import Optional, Any

tu =TrackingUtils()

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write(
            "Retrieving transactions and prices.."
        )
        trxs, pxs = tu.get_tracking_inputs()

        self.stdout.write("Tracking...")
        md = TrackingModel()
        trck = md.track(trxs)
        mrge = trck.merge(pxs, on=["securityid", "date"], how="left")
        mrge["mv"] = mrge.price.fillna(1) * mrge.qty
        psns = mrge[["accountid", "securityid", "date", "qty", "mv"]]


        self.stdout.write(
            "Saving positions..."
        )
        position(psns)
        self.stdout.write(
            self.style.SUCCESS(
                "Tracking complete!"
            )
        )
