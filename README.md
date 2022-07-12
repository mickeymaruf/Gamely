# Panda-Bazar
An E-commerce Game Store

## Installation
1. Copy files to your server and configure webserver
2. Install dependencies running the below from CLI (main project folder):
```shell
pip install -r requirements.txt
```
Note that I pinned django version to 4.0.x.
This is to make sure no updates are installed which could introduce breaking changes. Obviously this can easily be changed. 

3. Edit the `.sample-env` file in main directory

This file holds sensitive settings, which should not be pushed to git. Example content suitable for development/testing could be:
```shell
SECRET_KEY=''

EMAIL_HOST=''
EMAIL_PORT=''
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
EMAIL_USE_TLS=''
EMAIL_USE_TLS=''
STRIPE_PRIVATE_KEY=''
```
Visit https://djecrety.ir/ to GENERATE DJANGO SECRET KEY and put it in the SECRET_KEY value.
