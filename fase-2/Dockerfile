
FROM python:3.11-slim


WORKDIR /app


COPY requirements.txt .
COPY train.py .
COPY predict.py .


RUN pip install --upgrade pip && \
    pip install -r requirements.txt


RUN mkdir -p /app/data /app/artifacts

CMD ["bash"]