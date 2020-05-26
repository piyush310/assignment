FROM python:3.7

#install python module 
COPY . /application


WORKDIR /application

#install dependency
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "python","main.py"]
