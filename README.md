# StadtBank

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)

[Documents](https://oemersak.me/StadtBank/)

Basic Bank System with Web GUI and database

## Setup

### Create Environment (Optional)

To create a virtual environment, run the following command:

#### Activate virtual environment (for Unix-based systems)

```shell
python -m venv .venv
source .venv/bin/activate
```

#### Activate virtual environment (for Windows)

```shell
python -m venv .venv
.venv\scripts\activate
```

### Install Requirements

Install the required Python Modules

```shell
python -m pip install -r requirements.txt
```

## Create Database

To set up the database, perform the following step:

- Show up to migration files:

  ```shell
  python manage.py migrate
  ```

## Data Samples

You can use the [bin/randCus.py](bin/randCus.py) and [bin/randAct.py](bin/randAct.py) for generating sample data for your database.

## Running Server

After all setup, you can run the program with:

```shell
python manage.py runserver
```

> Use `--insecure` if you can't get Static Files

## Admin GUI

To access the admin GUI, you need to create a superuser account first. Run the following command:

```shell
python manage.py createsuperuser
```

> or you can run [bin/userSetup.py](bin/userSetup.py) for Account Setup

For access, you need to go to `http://IP_ADDRESS/admin`

> **Note:** Please ensure that your database migrations are applied before running the `createsuperuser` command.

## Compile Languages

StadtBank have a multi language system. You can find the translates in [Bank/locale](Bank/locale/). You need to compile them for the see Translates

```shell
python manage.py compilemessages
```

### Improve or add Translates

#### Improve Translates

You can change the `msgstr` in the `*.po` files. Every Text have a msgid and over them you can see where they used.

#### Add Translates

```shell
python manage.py makemessages -l LANGUAGE_CODE
```

## HTTPS Server

It is still in development. I'm not very good with it. Up now I only did what I found in internet for it.,
You can find the links in settings.py

### Create Certificates

You can run this command

```shell
openssl req -x509 -newkey rsa:4096 -keyout cets/server.key -out cers/server.pem -days 365 -nodes
```

or you can use the [certs/file.sh](certs/file.sh) for CA certificate

> CHECK THE CONFIGURATION IN [certs/file.sh](certs/file.sh) BEFORE RUN IT !!!

### Run Server

```shell
python manage.py runserver_plus --cert-file certs/server.pem --key-file certs/server.key --insecure 127.0.0.1:443
```
