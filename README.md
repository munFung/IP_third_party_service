# Setup
1. Download latest SQLite
````
https://sqlitebrowser.org/blog/version-3-13-0-released/
````
2. install dependencies
````
pip install -r requirements.txt
````
3. Use SQLite click *Open Database* > *[project_name]* > *instance* > *example.db*
- To view table record
4. Run the command below to run the Car Rental Service
````
python carService.py
````
5. Run the command below to run the Catering Package Service
````
python cateringPackage.py
````
6. Run the command below to run the Bank Service
````
python bankService.py
````
7. Run the command below to run the Account Maintenance Service
````
python ac_maintenance.py
````

## Notes:
### please keep the *ALL* server start when you need to fetch or modify the data from the service
All Service will run in different port number (from 5000 to 5004)
****
1. In PHP laravel
````
composer require guzzlehttp/guzzle
````
