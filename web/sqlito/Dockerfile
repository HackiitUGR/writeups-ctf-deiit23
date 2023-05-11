FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY app /app

COPY init.sh /

EXPOSE 6001

CMD [ "sh", "/init.sh" ]