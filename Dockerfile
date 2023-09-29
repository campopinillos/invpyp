FROM python:3.9.17
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 8050
CMD python dashapp.py