"""
This Add-On allows users to add tags or key/value pairs in bulk.
"""

import time
from documentcloud.addon import SoftTimeOutAddOn


class BulkTag(SoftTimeOutAddOn):
    """An example Add-On for DocumentCloud."""

    def main(self):
        """The main add-on functionality goes here."""
        # fetch your add-on specific data
        self.client.session.headers.update({'User-Agent': 'Bulk Tag Add-On'})
        key = self.data.get("key").strip()
        value = self.data.get("value").strip()

        for document in self.get_documents():
            if key in document.data:
                document.data[key].append(value)
                document.save()
            else:
                document.data[key] = value
                document.save()
            time.sleep(5)


if __name__ == "__main__":
    BulkTag().main()
