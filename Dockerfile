FROM python:3
ENV PYTHONBUFFERED 1
RUN mkdir /user_service
WORKDIR /user_service
COPY . /user_service/
RUN make setup_docker
