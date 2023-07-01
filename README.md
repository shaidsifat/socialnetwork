How to open project...

# pip install virtualenv 
python -m venv env
.env/Scripts/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
