FROM python

WORKDIR /project
COPY app.py requirements.txt database.py wait-for-it.sh ./

RUN chmod +x wait-for-it.sh
RUN pip install -r requirements.txt

ENV FLASK_APP=app.py
CMD flask run --host=0.0.0.0
