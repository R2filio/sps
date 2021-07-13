FROM python:3.7.5-slim
WORKDIR /usr/src/app
RUN python -m pip install \
        parse \
        realpython-reader

COPY .
RUN pip3 install -r rquirements.txt

CMD ["python3", "Monitor.py"]

