FROM hokiegeek2/python3

MAINTAINER hokiegeek2 hokiegeek2@gmail.com

RUN pip3 install chardet2 urllib3 requests

ADD checker-server.py /opt/checker-server.py
ADD health /opt/health
ADD utils /opt/utils

WORKDIR /opt

CMD python3 checker-server.py
