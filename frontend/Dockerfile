FROM python:3.10.11
WORKDIR /frontend
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
WORKDIR /frontend/src
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]