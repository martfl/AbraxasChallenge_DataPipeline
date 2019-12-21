FROM python:buster
RUN pip install requests redis
COPY get_data.py .
ENTRYPOINT ["python", "get_data.py"]
