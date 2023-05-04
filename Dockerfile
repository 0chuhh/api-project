FROM python:3
WORKDIR /apps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /apps
RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
