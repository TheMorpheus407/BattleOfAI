FROM python:3.7-stretch
WORKDIR /app/GameMicroservice
ADD . /app/GameMicroservice
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ENV PYTHONPATH="${PYTHONPATH}:/app:/app/GameMicroservice"
EXPOSE 80
ENV NAME GameMicroservice
CMD ["python", "app.py"]
