"""
This Add-On allows users to add tags or key/value pairs in bulk.
"""

from documentcloud.addon import AddOn

class BulkTag(AddOn):
    """An example Add-On for DocumentCloud."""

    def main(self):
        """The main add-on functionality goes here."""
        # fetch your add-on specific data
        if not self.documents:
            self.set_message("Please select at least one document.")
            return
            
        key = self.data.get("key").strip()
        value = self.data.get("value").strip()
    
        for document in self.get_documents():
            if key in document.data:
                document.data[key].append(value)
                document.save()
            else:
                document.data[key] = value
                document.save()


if __name__ == "__main__":
    BulkTag().main()
