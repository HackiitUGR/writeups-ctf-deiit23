FROM python:3

WORKDIR /urs/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt \
    && mkdir static

EXPOSE 5002
ENV FLASK_RUN_HOST 0.0.0.0

ENV FLASK_APP "introsp3ctiv3.py"
ENV FLASK_RUN_PORT 5002

ENTRYPOINT ["flask", "run"]