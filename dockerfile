FROM python:3.10-slim

# set the working directory
WORKDIR /src
# install dependencies
COPY ./requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the src to the folder

EXPOSE 8000

COPY ./src ./src

# start the server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0" , "--port", "8000", "--reload"]
