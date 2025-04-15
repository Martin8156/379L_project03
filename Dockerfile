# Image: martinbrianinfante/ml-houses-api

FROM python:3.11

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY models /models
COPY data /data
COPY api.py /api.py

CMD ["python", "api.py"]