FROM python:3.10-slim

# set the working directory
WORKDIR /app

#copy working directory
COPY . /app

RUN sudo apt-get install libmysqlclient-dev

# install dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# exit root
USER 1000:1000

# expose port
EXPOSE 8080

# start the server
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0" , "--port", "8080", "--reload"]
