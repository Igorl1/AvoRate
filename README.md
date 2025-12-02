# AvoRate
Repository made in 2025.2 for the Software Engineering (INF1041) course at PUC-Rio.

# How to Run Locally
- It's recommended to download the latest Python version (https://www.python.org/downloads/)

- Clone the project
```
git clone https://github.com/Igorl1/AvoRate/
```

- Create a virtual environment
```
> cd AvoRate/server
> On Linux:
python3 -m venv .venv
source .venv/bin/activate
> On Windows:
python -m venv .venv
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned  # Might need to use it one time
.\.venv\Scripts\activate
> pip install -r requirements.txt
```

- Run flask
```
> Run only for your PC:
flask run --debug  # Debug ensures the server will automatically reload if code changes (not for production)
> Run for all users in your network:
flask run --debug --host=0.0.0.0
```

# Before Commiting
- Run ruff on server folder
```
# Check for issues
ruff check .

# Apply automatic formatting and fixes
ruff format .
```