# Set up the database 
Set the database configuration into the `config\setting.py`

# How to start application
1. python -m venv env
2. source env/bin/activate , .\env\Scripts\Activate
3. Install the dependencies usind `pip install -r requirements.txt`
4. run command to update database
  -> alembic revision --autogenerate -m "your message"
  -> alembic upgrade head
5. Run `uvicorn app:app --reload`




.\env\Scripts\Activate
uvicorn main:app --host 0.0.0.0 --port 8000
