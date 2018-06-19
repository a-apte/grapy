## Grapy

This program matches wines from vendor websites with Vivino ratings. It allows 
you to add plugins to scrape wine lists from vendors. Wines are persisted in a 
datastore. Rating scrapers can then be used to scrape ratings for your wine 
lists.

Based on Django DRF


### Code structure

* grapy/: the Django configuration
* plugins/: all the vendor and rating plugins
* scraper/: code that runs the scraping plugins
* test/: unit tests
* wines/: the Django model description
* wines/fixtures/: initial model data with countries, vendors and raters
* wines/migrations/: Django migration files to setup the database -- remove??
* grapy.py: main module
* logging.json: logging configuration file
* manage.py: commands to manage Django configuration
* README.md: project description file
* requirements.txt: dependencies to other python modules


### Model description

#### Wine details:
* name: the name of the wine.
* winetype: what type of wine is it? wine, port, etc.
* color: red, white, rose
* country: the origin country, from the list of (countries)[/wines/fixtures/countries.json]
* region: the origin region
* winery: the winery that produces the wine
* modified: timestamp of last update

#### For a specific vendor, the following details can be captured:
* vendor_code: the unique code of the wine for this vendor
* volume = contents of the bottle
* quantity = number of bottles
* price = advertised price
* url = URL to the wine's product page
* modified = timestamp of last update

#### Vendor:
* name: unique vendor name
* url: URL to the vendor website
* is_active: enable or disable scraping for this vendor
* is_test: in test mode, no products are persisted in the datastore
* plugin: filename of the .py plugin file in the plugins folder
* page: relative path from the url to the wine list page
* max_pages: maximum number of product pages to scrape
* product: css class or id that identifies a product on a product page
* stopwords: product names containing a stopword are filtered from the resultset



### Adding more plugins

All plugins must extend the class PluginBase in plugins/pluginbase.py

Vendor plugins must return the following product details:

* vendor_id: automatically
* code: the unique code of the wine for this vendor
* title: the name of the wine.
* url: URL to the wine's product page
* winetype: what type of wine is it? wine, port, etc.
* color: red, white, rose
* volume: contents of the bottle
* quantity: number of bottles
* price: advertised price


### Commands


#### Setup
Prepare database:
```python manage.py makemigrations```
-- migrations folder is dan niet meer nodig


Sync database:
```python manage.py migrate```


Create super user:
```python manage.py createsuperuser --email admin@example.com --username admin```


Run tests
```python -m unittest```


Load data
```python manage.py loaddata countries.json```


Start server
```python manage.py runserver```


#### Admin

Update requirements.txt
```pipreqs . --force```

Dump data
```python manage.py dumpdata wines.country > countries.json```

