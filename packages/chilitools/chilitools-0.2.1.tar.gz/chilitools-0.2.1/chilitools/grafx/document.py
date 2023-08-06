import json

class GraFxDocument:
    def __init__(self, doc: str, id: str = None, name: str = None):
        try:
            # We were passed a parsed JSON document
            if isinstance(doc, dict):
                self.doc = doc
            # We were passed the raw JSON string of the document
            if isinstance(doc, str):
                self.doc = json.loads(doc)
        except Exception as e:
            self.doc = {}
            print(f"FAILURE PARSING GRAFX DOCUMENT: {e}")

        if id: self.id = id
        if name: self.name = name

    @property
    def json(self): return str(self)

    @property
    def images(self):
      image_frames = []
      for page in self.doc["pages"]:
          for frame in page["frames"]:
              # Todo(austin): Figure out how the hell you want to handle this
              if frame["frameType"] == "image":
                    # Image is coming from a connector
                    if frame["src"].get("connectorId") == "grafx-media":
                        image_frames.append(frame)
                    # Image is is a variable
                    if frame["src"].get("variableId"):
                        # Find and get the asset Id from the variable
                        for var in self.doc["variables"]:
                            if var.get("id") == frame["src"].get("variableId"):
                                frame["src"]["assetId"] = var["src"]["assetId"]
      return image_frames

    def __str__(self): return json.dumps(self.doc)
    def __repr__(self): return self.doc