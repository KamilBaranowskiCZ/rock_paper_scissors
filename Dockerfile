FROM python:3.8
COPY . /game
WORKDIR /game
RUN pip install -r ./requirements.txt
ENTRYPOINT ["python"]
CMD ["run.py"]