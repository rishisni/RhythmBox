# frontend

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


# backend

# create virtual environment
python3 -m venv env

# activate by using this command
source env/bin/activate

# Install dependencies:
pip install -r requirements.txt

# run 
python3 app.py


# To run redis server
redis-server

# To run clery jobs 
celery -A app:celery worker --loglevel=info
celery -A app:celery beat --loglevel=info