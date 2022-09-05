FROM python:alpine3.16

WORKDIR /usr/src/api

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0"]