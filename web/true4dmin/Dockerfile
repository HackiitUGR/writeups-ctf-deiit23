FROM python:3

WORKDIR /urs/src/app

COPY . .
RUN mkdir db
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP true4dmin.py
ENV FLASK_ENV production
ENV SECRET_KEY sup3rs3cr3tk3y!

CMD ["sh", "-c", "python db.py && flask run --host=0.0.0.0"]

