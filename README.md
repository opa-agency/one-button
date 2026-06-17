# one-button

primi 10 de platitori 


# Setup Commands
python3 -m venv .venv
source .venv/bin/activate
pip install pip --upgrade
pip install -r requirements.txt
pip install -r requirements.dev.txt
python manage.py tailwind install
python manage.py tailwind start

# optional admin bootstrap on container start
# set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD




# default: one fake paid user every 5s, forever
python manage.py simulate_payments

# every 2s
python manage.py simulate_payments --interval 2

# stop after 10
python manage.py simulate_payments --count 10

# clear previously-simulated rows first
python manage.py simulate_payments --interval 2 --clear