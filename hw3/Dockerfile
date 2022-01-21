FROM python:3.8

WORKDIR /

COPY src/ /src/
COPY setup.py .

RUN pip install -e .

CMD [ "jarvis" ]