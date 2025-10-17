FROM python:3.12-slim
WORKDIR /Artiukhov
COPY . /Artiukhov
RUN pip install --no-cache-dir deep-translator langdetect googletrans==3.1.0a0
CMD ["python", "gtrans3.py"]
