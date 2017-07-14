import os
import base64
import sys
import json
import googleapiclient.discovery
from PIL import Image
import io
import httplib2

from urllib.request import urlopen
from flask import Flask, render_template, request
app = Flask(__name__)

ML_SERVICE = googleapiclient.discovery.build("ml", "v1")

def build_request(http, *args, **kwargs):
  new_http = httplib2.Http()
  return apiclient.http.HttpRequest(new_http, *args, **kwargs)

@app.route("/", methods=["GET"])
def home():
  return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def predict():
  payload = json.loads(request.data.decode("utf-8"))
  img = None
  if "fileUrl" in payload:
    img = base64.b64encode(urlopen(payload.get("fileUrl")).read())
  elif "fileBinary" in payload:
    img = payload.get("fileBinary", None).split(",")[1]
  else:
    return "{\"error\": \"no image\"}", 400

  # Read in image as an Image in memory
  buff = Image.open(io.BytesIO(base64.b64decode(img)))

  # Convert image to JPEG
  out_buff = io.BytesIO()
  buff.convert("RGB").save(out_buff, format="JPEG")

  # Output image as base64
  out_buff.seek(0)
  img = base64.b64encode((out_buff.getvalue())).decode("ascii")

  service = googleapiclient.discovery.build("ml", "v1", requestBuilder=build_request)
  resp = ML_SERVICE.projects().predict(
      name="projects/jcham-1469824226729/models/hotdog",
      body={
          "instances": [{
              "key": "0",
              "image_bytes": {
                  "b64": img,
              },
          }]
      }).execute()
  print(resp)
  return json.dumps(resp)



#if __name__ == "__main__":
#  app.run()

