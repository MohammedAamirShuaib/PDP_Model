FROM python:3.7.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY pdp_model.py .
COPY main.py .
EXPOSE 8000