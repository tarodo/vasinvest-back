# VASInvest
## Project for my sister
I want to show my sister how investments work. How to start investing at 15 to gain financial independence as early as possible.
____
This is the backend for the service.
____
## To start
1. ```pip install -r requirements.txt```
1. Create .env by ```cp .env.Example .env```
1. ```uvicorn main:app```
1. Create SU by ```python create_su.py```

## To test
1. ```pytest --cov="."```

## Preparing new code
1. ```flake8 .```
1. ```black .```
1. ```isort .```