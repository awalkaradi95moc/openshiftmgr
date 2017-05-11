# Docker file for the openshift manager

FROM fnndsc/ubuntu-python3:latest
MAINTAINER fnndsc "dev@babymri.org"

ENV APPROOT="/usr/src/openshift"  VERSION="0.1"
COPY ["openshift.py", "test_openshift.py", "requirements.txt", "${APPROOT}/"]

WORKDIR $APPROOT

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["openshift.py", "--help"]