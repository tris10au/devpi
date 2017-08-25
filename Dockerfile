FROM centos:7

RUN yum upgrade -y && \
    yum install -y epel-release && \
    yum install -y pypy && \
    mkdir -p /app

WORKDIR /app

COPY dev_pi.py /app/dev_pi.py

CMD [ "pypy", "/app/dev_pi.py" ]
