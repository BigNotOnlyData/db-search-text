FROM python:3.10.11
WORKDIR /backend
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./src /backend/src
COPY ./data /backend/data
WORKDIR /backend/src
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]