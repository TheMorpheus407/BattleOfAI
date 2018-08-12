FROM python:3.7-stretch
WORKDIR /app/AccountManagement
ADD . /app/AccountManagement
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ENV PYTHONPATH="${PYTHONPATH}:/app:/app/AccountManagement"
EXPOSE 80
ENV NAME AccountManagement
CMD ["python", "app.py"]
