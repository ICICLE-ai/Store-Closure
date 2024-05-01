FROM python:3

WORKDIR /abm-app

COPY requirements.txt /abm-app/

#install requirements
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /abm-app/

CMD ["python3", "main.py"]