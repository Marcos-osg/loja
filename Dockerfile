FROM python:3.9

RUN mkdir /backend
WORKDIR /backend
COPY . .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install gunicorn

CMD ["gunicorn", "loja.wsgi:application", "--bind", "0.0.0.0:8000"]