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

# Setting up Django Project using Nginx and Gunicorn
1. Use `git clone` to download project locally to linux server
2. Setup like you would locally, and try `runserver` then visit `YOUR_IP_ADDRESS:8000` to verify that it works.
3. Setup Gunicorn: Do `gunicorn --bind 0.0.0.0:8000 garage-scooterson.wsgi` to start gunicorn server (note that garage-scooterson should be the file containing manage.py)
4. Setup Supervisor: 
    1. Install it on your server via `sudo apt install supervisor`
    2. Create a config file via `sudo nano /etc/supervisor/conf.d/garage-scooterson.conf`
    3. Add this to the config file: 
    ```
    [program:garage-scooterson]
    command=/path/to/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 garage-scooterson.wsgi
            directory=/path/to/garage-scooterson/directory
            autostart=true
            autorestart=true
            stderr_logfile=/var/log/garage-scooterson/stderr.log
            stdout_logfile=/var/log/garage-scooterson/stdout.log
            user=root
    ```
    4. Run: 
    ```
    sudo supervisorctl reread
            sudo supervisorctl update
            sudo supervisorctl restart garage-scooterson
    ```
5. Setup Nginx as a reverse proxy
    1. Install via: `sudo apt install nginx`
    2. Creat Nginx server block config file via `sudo nano /etc/nginx/sites-available/garage-scooterson`
    3. Add this to your file:
    ```        
        server {
            listen 80;
            server_name YOUR_DOMAIN/IP;

            location / {
                -- this should be the localhost, NOT yoru IP
                proxy_pass http://127.0.0.1:8000;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            }

            location /static/ {
                alias /path/to/garage-scooterson/directory/static/;
            }

            location /media/ {
                alias /path/to/garage-scooterson/directory/media/;
            }
        }
    ```
    4. Enable this site via : `sudo ln -s /etc/nginx/sites-available/garage-scooterson /etc/nginx/sites-enabled/`
    5. Test the nginx proxy via `sudo nginx -t` then do `sudo service nginx restart`
6. Configure firewall :
    ```
    sudo ufw allow 22  # Allow SSH
    sudo ufw allow 80  # Allow HTTP
    sudo ufw enable
    ```
7. Setup domain on DO panel AND request for SSL certificate via Let's Cert