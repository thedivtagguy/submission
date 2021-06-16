from flask import Flask, request, render_template
import os
from .extensions import register_extensions, assets
from contentful_management import Client
import hashlib
import random

atoken = os.environ.get("ACCESS_TOKEN")
space = os.environ.get("SPACE_ID")

def create_app():
    app = Flask(__name__)   
    assets._named_bundles = {}
    register_extensions(app)

    @app.route("/", methods =["GET", "POST"])
    def index():
        if request.method == "POST":
           #  Get User Details
            authorname = request.form["name"]
            email = request.form["email"] 
            major = request.form["major"]
            tools_list = request.form["tools"]
            tools_list = tools_list.split(",")
            year_study = request.form["year"]
            project_title = request.form["projectname"]
            project_description = request.form["projectdescription"]
            no_files = request.form["filenumber"]
            client = Client(atoken)

            # Entry ID Generation
            uid = hashlib.md5(project_title.encode())
            uid = uid.hexdigest()
            uid = list(uid)
            random.shuffle(uid)
            uid = ''.join(uid)

            # File Counter
            x = 0 

            # Array for File IDs
            files_array = []
            while x < int(no_files):
                  fieldid = "file" + str(x)
                  file_name = "filename" + str(x)
                  fname = request.form[file_name]
                  uid2 = hashlib.md5(fname.encode())
                  uid2 = uid2.hexdigest()
                  uid2 = list(uid2)
                  random.shuffle(uid2)
                  uid2 = ''.join(uid2)
                  uploadmedia = request.files[fieldid]
                  # Upload File
                  new_upload = client.uploads(space).create(uploadmedia.stream)  
                  # Upload to Asset             
                  client.assets(space, 'master').create(uid2,
                     {
                     'fields': {
                         'title': {
                           'en-US': fname
                           },
                        'file': {
                           'en-US': {
                           'fileName': file_name,
                           'contentType': uploadmedia.content_type,
                           'uploadFrom': new_upload.to_link().to_json()
                           }
                        }
                     }
                     }
                  )
                  
                  # Process and Publish Asset
                  asset = client.assets(space, 'master').find(uid2)
                  asset.process()
                  asset.publish() 
                  x = x + 1
                  files_array.append(uid2)
            
            # Generate ID List
            ids = []
            for asset_id in files_array:
               y = asset_id
               x = {"sys": {"type": "Link", "linkType": "Asset", "id": y}}
               ids.append(x)
          
            # Create an Entry:
            entry_id = uid  
            entry = client.entries(space, 'master').create(entry_id, {
              'content_type_id': 'portfolio',
               "fields": {
                "name": {
                   "en-US":  project_title,
                },
                "author": {
                   "en-US":  authorname,
                },
                "contact": {
                   "en-US":  email,
                },
                "major": {
                   "en-US":  major,
                },
                "tools": {
                   "en-US":  tools_list,
                },
                "year": {
                   "en-US":  year_study,
                },
                "slug": {
                   "en-US":  project_title,
                },
                "description": {
                   "en-US":  project_description,
                },
                 "files":{
                  "en-US" : ids
                 } 
                } })
                  # Update the Entry:
            entry.title = project_title
            entry.save()
        return render_template("index.html") # print(uploadmedia.filename)
    
    return app

