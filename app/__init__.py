from flask import Flask, request, render_template, redirect, url_for
import os
from .extensions import register_extensions, assets
from .mail import send_email
from contentful_management import Client
import uuid
from slugify import slugify
import time

atoken = os.environ.get("ACCESS_TOKEN")
space = os.environ.get("SPACE_ID")

def create_app():
    app = Flask(__name__)   
    assets._named_bundles = {}
    register_extensions(app)
    @app.route('/success')
    def success():
      # replace this with a query from whatever database you're using
      # access the result in the tempalte, for example {{ result.name }}
      return render_template('success.html')
      
    @app.route("/", methods =["GET", "POST"])
    def index():
       
        uid = uuid.uuid4().hex[:10] 
        if request.method == "POST":
           #  Get User Details
            authorname = request.form["name"]
            email = request.form["email"] 
            major = request.form["major"]
            tools_list = request.form["tools"]
            tools_list = tools_list.split(",")
            year_study = request.form["year"]
            project_cat = request.form['project_category']
            project_title = request.form["projectname"]
            course_name = request.form["course"]
            project_description = request.form["projectdescription"]
            no_files = request.form["filenumber"]
            client = Client(atoken)
            #   This is the Entry ID

            slug = slugify(project_title)
            slug_id = uid[-4:]
            slug = slug + "-" + slug_id
            # File Counter
            x = 0 
            

            # Array for File IDs
            files_array = []
            while x < int(no_files):
                  fieldid = "file" + str(x)
                  file_name = "filename" + str(x)
                  fname = request.form[file_name]
                  asset_id = uuid.uuid4().hex[:20] 
                  files_array.append(asset_id)
                  uploadmedia = request.files[fieldid]
                  # Upload File
                  new_upload = client.uploads(space).create(uploadmedia.stream)  
                  # Upload to Asset             
                  client.assets(space, 'master').create(asset_id,
                     {
                     'fields': {
                         'title': {
                           'en-US': fname
                           },
                        'file': {
                           'en-US': {
                           'fileName': uid,
                           'contentType': uploadmedia.content_type,
                           'uploadFrom': new_upload.to_link().to_json()
                           }
                        }
                     }
                   }
                  )
                  
                  # Process and Publish Asset
                  asset = client.assets(space, 'master').find(asset_id)
                  asset.process()
                  time.sleep(4) # Number of seconds
                  asset.reload().publish() 
                  x = x + 1
            
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
                   "en-US":  slug,
                },
                "description": {
                   "en-US":  project_description,
                },
                "category": {
                   "en-US":  project_cat,
                },
                "course": {
                   "en-US":  course_name,
                },
                 "files":{
                  "en-US" :  ids
                 } 
                } })
                  # Update the Entry:a
            entry.reload()
            entry.title = project_title
            entry.save()
            entry.reload()
            send_email(email, uid, project_title)
            return redirect(url_for('success'))

        return render_template("index.html", unique_id = uid) # print(uploadmedia.filename)
    
    return app

