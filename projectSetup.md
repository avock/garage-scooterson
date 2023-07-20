# Updating an outdated table (changes to schema)
1. run ```python3 manage.py makemigrations garageApp```
2. drop all related tables
3. run ```python3 manage.py migrate --fake garageApp zero```, this sets migration to fake
4. run ```python3 manage.py migrate garageApp```

# Starting virtual environment
1. Go into garage-env directory
2. run `source bin/activate`

# Installing dependencies
1. Go into root directory
2. Start virtual environment
3. Update all dependencies in `garage-env/requirements.txt`
4. run `python3 -m pip install -r garage-env/requirements.txt`

# Server Commands for Digital Ocean
- `sudo systemctl start nginx`
- `sudo systemctl stop nginx`
- `sudo systemctl restart nginx` : stops and starts service again
- `sudo systemctl reload nginx`: reloads without dropping connection (only for configuration changes)
- `sudo systemctl disable nginx`: disable nginx starting when server boots up (alternatively `enable`)