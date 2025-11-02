FROM python:3.10-slim

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install mysql-connector-python

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]
