"""
This Add-On allows users to add tags or key/value pairs in bulk.
"""

import sys
import time
from itertools import batched

from documentcloud.addon import SoftTimeOutAddOn
from documentcloud.exceptions import APIError

BATCH_SIZE = 25


class BulkTag(SoftTimeOutAddOn):
    """Add-On that bulk tags documents 25 at a time"""

    def tag_documents(self, payload, max_retries=5, retry_delay=60):
        """Bulk tag a batch of documents. Retry on failure"""
        retries = 0
        while retries < max_retries:
            try:
                print(f"Tagging batch of {len(payload)} documents...")
                self.client.patch("documents/", json=payload)
                print("Finished tagging batch")
                return
            except APIError as exc:
                print(f"Error tagging batch. {exc}. Retrying...")
                retries += 1
                time.sleep(retry_delay)
        # Retries exhausted
        print(f"Failed to tag batch after {max_retries} attempts.")
        self.set_message(
            "Failed to set tags for some documents. "
            "Email info@documentcloud.org to debug."
        )
        sys.exit(1)

    def main(self):
        """Set user agent, get keys and values, then tag in batches"""
        self.client.session.headers.update({"User-Agent": "Bulk Tag Add-On"})
        key = self.data.get("key").strip()
        value = self.data.get("value").strip()

        for chunk in batched(self.get_documents(), BATCH_SIZE):
            payload = [{"id": document.id, "data": {key: value}} for document in chunk]
            if payload:
                self.tag_documents(payload)


if __name__ == "__main__":
    BulkTag().main()
