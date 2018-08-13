FROM python:3.7-stretch
WORKDIR /app/AccountManagement
ADD . /app/AccountManagement
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ENV PYTHONPATH="${PYTHONPATH}:/app:/app/AccountManagement"
EXPOSE 80
ENV NAME AccountManagement
ENV DB_HOSTNAME localhost
ENV DB_PORT 3306
ENV DB_USERNAME boai
ENV DB_DATABASE boai
ENV SMTP_HOST localhost
ENV SMTP_PORT 587
CMD ["python", "app.py"]
