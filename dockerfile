FROM python:3.10-slim

# exit root
RUN net user /add api
USER api

# set the working directory
WORKDIR /app

#copy working directory
COPY . /app

# install dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# expose port
EXPOSE 8080

# start the server
ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0" , "--port", "8080", "--reload"]
