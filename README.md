# Running & Testing
`uvicorn main:app --reload`


## i need to do
- postgresql
- uv
- docker 
- celery

# Project Structure (directory tree)
```
techtask
    |
    ---app
        ├── __init__.py
        ├── core
        │   ├── __init__.py
        │   ├── db.py
        │   ├── logging.py
        │   └── security.py
        ├── depends.py
        ├── main.py
        ├── models
        │   ├── __init__.py
        │   ├── pizza.py
        │   ├── restaurant.py
        │   └── review.py
        ├── routers
        │   ├── __init__.py
        │   ├── main_router.py
        │   ├── pizza_router.py
        │   ├── restaurant_router.py
        │   └── review_router.py
        ├── schemas
        │   ├── __init__.py
        │   ├── pizza.py
        │   ├── restaurant.py
        │   └── review.py
        ├── services
        │   ├── __init__.py
        │   ├── pizza
        │   │   └── pizza_service.py
        │   ├── restaurant
        │   │   └── restaurant_service.py
        │   ├── review
        │   │   └── review_service.py
        │   └── seed.py
        └── tests
            ├── __init__.py
            ├── pizza
            │   ├── test_pizza_endpoints.py
            │   └── test_pizza_service.py
            ├── restaurant
            ├── review
            └── test_main.py
    -README.md
    -requirements.txt
```


