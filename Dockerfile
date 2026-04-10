<<<<<<< HEAD
FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

=======
FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

>>>>>>> 1ae9310eb78a0f51dd8f99df9bac2725c9351cc8
CMD ["python", "src/solar_model.py"]