FROM debian
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 80/tcp
WORKDIR /app/
COPY . .
RUN apt-get update && apt-get -y --no-install-recommends install python3-minimal python3-setuptools python3-pip
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*
RUN python3 -m pip install --no-cache-dir -r requirements.txt
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:80" ]
