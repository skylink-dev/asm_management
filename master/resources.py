from decimal import Decimal
from import_export import resources, fields
from import_export.widgets import DecimalWidget
from .models import PincodeData


class CustomDecimalWidget(DecimalWidget):
    """
    Treat common placeholders as empty/NULL so Decimal conversion doesn't fail.
    Returns None for blank/"NA"/"N/A"/"-"/"NULL"/"NONE".
    If you prefer 0.0 instead of None, change `return None` to `return Decimal('0.0')`.
    """
    def clean(self, value, row=None, *args, **kwargs):
        # normalize
        if value is None:
            return None
        v = str(value).strip()

        if v == "":
            return None

        # common placeholders you might see in CSV/Excel
        if v.upper() in ("NA", "N/A", "-", "NULL", "NONE"):
            return None

        # If still something, delegate to parent (it will sanitize separators and Decimal() it)
        try:
            return super().clean(v, row=row, *args, **kwargs)
        except Exception:
            # fallback: return None so import continues (avoid crashing)
            return None


class PincodeDataResource(resources.ModelResource):
    latitude = fields.Field(
        column_name="latitude",
        attribute="latitude",
        widget=CustomDecimalWidget()
    )
    longitude = fields.Field(
        column_name="longitude",
        attribute="longitude",
        widget=CustomDecimalWidget()
    )

    class Meta:
        model = PincodeData
        # pick unique keys that identify a row for updates (adjust if needed)
        import_id_fields = ("pincode", "officename")
        fields = (
            "circlename", "regionname", "divisionname", "officename", "pincode",
            "officetype", "delivery", "district", "statename", "latitude", "longitude"
        )
        skip_unchanged = True
        report_skipped = True
