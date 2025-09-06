To Generate virtual env 
python -m venv venv

To activate venv
<Path>\venv\Scripts\activate  


Python pacakages
pip install fastapi uvicorn sqlalchemy bcrypt jinja2


pip install "fastapi[all]"
pip install python-jose[cryptography] passlib[bcrypt]



To Start service

( in background for poweshell)
Start-Process powershell -ArgumentList "uvicorn main:app --reload"

(in background for linux)
nohup uvicorn main:app --reload &

( in foreground)
uvicorn main:app --reload