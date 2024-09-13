# workspace
A workspace for the nieces
So far includes hello world in a few languages plus some assets


# Python virtualenv usage
# Note, commonly one might use ~/.venv as ${folder_name} below
*Create one
  python3 -m venv ${folder_name}
* Use it
  source ${folder_name}/bin/activate
* Update requirements.txt - back up your current environment's libraries.
  pip freeze > requirements.txt
* Update it (assumes you have a requirements.txt file
  pip install -r requirements.txt
* Shut it down
  deactivate

Keeping a requirements.txt file is handy if you switch computers a lot

