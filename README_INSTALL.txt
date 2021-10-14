From source run:
pip freeze > requirements.txt

From target run:
pip install -r requirements.txt

Change any wheels to the current location

PySpark will not work if just pulled from GitHub. Recreate each model in the target 