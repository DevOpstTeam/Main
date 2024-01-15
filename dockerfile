FROM python:3.10-slim

# set the working directory
WORKDIR /app
# install dependencies
COPY . /app
run pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# copy the src to the folder

EXPOSE 8080



# start the server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0" , "--port", "8080", "--reload"]
