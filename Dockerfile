FROM python:3.13-slim

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY ./.env /app/

COPY ./storeapi /app/storeapi/


EXPOSE 8000

CMD ["uvicorn","storeapi.main:app","--host","0.0.0.0","--port","8000"]
