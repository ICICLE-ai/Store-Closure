FROM python:3.8

#install gdal and libspatialindex
RUN apt-get update && apt-get install --yes libgdal-dev && apt-get install --yes libspatialindex-dev

WORKDIR /abm-app

COPY requirements.txt /abm-app/

#install requirements
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /abm-app/

CMD ["python3", "run.py"]