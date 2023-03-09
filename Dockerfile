# Prepare the base environment.
FROM ubuntu:22.04 as builder_base_encryptiongw
MAINTAINER asi@dbca.wa.gov.au
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Australia/Perth
ENV PRODUCTION_EMAIL=True
ENV SECRET_KEY="ThisisNotRealKey"
# Key for Build purposes only
ENV FIELD_ENCRYPTION_KEY="Mv12YKHFm4WgTXMqvnoUUMZPpxx1ZnlFkfGzwactcdM="
# Key for Build purposes only
RUN apt-get clean
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install --no-install-recommends -y wget git libmagic-dev gcc binutils libproj-dev gdal-bin python3 python3-setuptools python3-dev python3-pip tzdata cron rsyslog python3-pil
RUN apt-get install --no-install-recommends -y libpq-dev patch
RUN apt-get install --no-install-recommends -y postgresql-client mtr
RUN apt-get install --no-install-recommends -y sqlite3 vim postgresql-client ssh htop
RUN ln -s /usr/bin/python3 /usr/bin/python 


COPY timezone /etc/timezone
ENV TZ=Australia/Perth
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY cron /etc/cron.d/dockercron
COPY startup.sh /
RUN chmod 0644 /etc/cron.d/dockercron
RUN crontab /etc/cron.d/dockercron
RUN touch /var/log/cron.log
RUN service cron start
RUN chmod 755 /startup.sh


RUN groupadd -g 5000 oim
RUN useradd -g 5000 -u 5000 oim -s /bin/bash -d /app
RUN mkdir /app
RUN chown -R oim.oim /app
USER oim

RUN pip install --upgrade pip
# Install Python libs from requirements.txt.
FROM builder_base_encryptiongw as python_libs_encryptiongw
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt 
RUN rm -rf /var/lib/{apt,dpkg,cache,log}/ /tmp/* /var/tmp/*


# Install the project (ensure that frontend projects have been built prior to this step).
FROM python_libs_encryptiongw
COPY gunicorn.ini /app
RUN touch /app/.env
COPY .git /app/.git
COPY encryptiongw /app/encryptiongw
COPY manage.py /app
RUN ls -la /app/
RUN ls -al /app/encryptiongw/
RUN mkdir /app/encryptiongw/cache/
RUN chmod 777 /app/encryptiongw/cache/
RUN python manage.py collectstatic --noinput
EXPOSE 8080
HEALTHCHECK --interval=1m --timeout=5s --start-period=10s --retries=3 CMD ["wget", "-q", "-O", "-", "http://localhost:8080/"]
CMD ["/startup.sh"]