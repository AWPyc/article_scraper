FROM python:3.13.9

ARG USER_ID=1000
ARG GROUP_ID=1000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN groupadd -g $GROUP_ID -o user && useradd -m -u $USER_ID -g user user

RUN apt-get update -y && apt-get install -y && apt-get install -y netcat-traditional

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install-deps

WORKDIR /article_scraper

COPY ./article_scraper .

RUN mkdir logs && chown -R $USER_ID:$GROUP_ID .

EXPOSE 8000

USER user

RUN playwright install
