FROM python:3.7.0
ADD requirements.txt ./
RUN pip install -r requirements.txt
ADD my_pow_syndacoin.py ./
ADD utils.py ./
ADD identities.py ./

CMD ["python", "-u", "my_pow_syndacoin.py", "serve"]
