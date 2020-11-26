FROM python:3.8.5
ADD . /app
WORKDIR /app
COPY /myscript.sh /myscript.sh
RUN pip install -r requirements.txt
RUN chmod +x app/myscript.sh
