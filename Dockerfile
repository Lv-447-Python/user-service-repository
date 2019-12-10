FROM python:3
ENV PYTHONBUFFERED 1
RUN mkdir /user_service
WORKDIR /user_service
COPY requirements.txt /user_service/
RUN pip install -r requirements.txt
COPY . /user_service/
