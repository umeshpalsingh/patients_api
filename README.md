# patients_api

A FastAPI project for managing patient records.

## Run locally on Windows

Run these commands from the project directory in PowerShell.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
fastapi dev main.py
```

Open [Swagger UI](http://127.0.0.1:8000/docs) to try the API. The API starts with an empty dataset and creates `patients.json` when you add the first record. Git ignores this file so the records stay local.
