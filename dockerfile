FROM python:3.12.0
RUN pip install --upgrade pip

WORKDIR /ThroneAPI
COPY ./requirements.txt /ThroneAPI/
RUN pip install -r requirements.txt

COPY . /ThroneAPI/
EXPOSE 8000

CMD ["uvicorn", "ThroneAPI:app", "--host", "0.0.0.0", "--port", "8000"]