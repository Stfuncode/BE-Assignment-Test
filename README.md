# BE Assignment

## Installation
1. Clone
```
git clone https://github.com/Stfuncode/BE-Assignment-Test.git

cd be-assignment-test
```

2. Create a virtual environment
```
python -m venv ./venv
```

3. Activate virtual environment

Windows
```
venv\Scripts\activate
```
macOS/Linux:
```
source venv/bin/activate
```

4. Install Dependency
```
pip install -r requirements.txt
```

5. Setup DB
```
python manage.py migrate
```

6. Create Superuser
```
python manage.py createsuperuser
```

7. Start server
```
python manage.py runserver
```

## Pages
- `/admin`
- `/inventory`
- `/inventory/<id>`

## Admin Panel
Access admin page `/admin` to add new inventory and supplier.

## API Endpoint
1. GET /api/v1/inventory

Retrieves a list of inventory items. You can filter by query parameters provided below
```
- name : <str>
- supplier : <str>
- stock : <int>
- availability : <bool>
```

## Unit Test
Test included:
- InventoryService unit test
- InventoryListView unit test
- InventoryDetailView unit test
- InventoryListApiView unit test

To run unit test:
```
python manage.py test
```
