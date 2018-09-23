FROM python:3.7-stretch
WORKDIR /app/GameMicroservice
ADD . /app/GameMicroservice
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ENV PYTHONPATH="${PYTHONPATH}:/app:/app/GameMicroservice"
EXPOSE 80
ENV NAME GameMicroservice
ENV DB_HOSTNAME localhost
ENV DB_PORT 3306
ENV DB_USERNAME boai
ENV DB_DATABASE boai
CMD ["python", "app.py"]
