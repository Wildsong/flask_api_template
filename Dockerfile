# I got tired of the continuum conda image not working quite right
# so I build my own now.
# This basic Flask-in-Docker image is used in several other projects now.
FROM debian:11
LABEL maintainer="Brian Wilson <brian@wildsong.biz>"
LABEL version="1.0"
LABEL biz.wildsong.name="flask"

ENV SERVER_BASE /srv

# Don't run as root
ENV CONDA="/home/app/miniconda3"
RUN adduser --disabled-password --gecos '' app
WORKDIR /home/app
ENV INSTALLER Miniconda3-latest-Linux-x86_64.sh
ADD https://repo.continuum.io/miniconda/${INSTALLER} .
RUN chmod 755 ${INSTALLER}
USER app
RUN sh ./${INSTALLER} -b && \
    rm ./${INSTALLER}
ENV PATH=${CONDA}/bin/:${PATH}

# Install the packages that this project needs.
COPY requirements.txt .
RUN conda config --add channels conda-forge &&\
    conda install -y --file requirements.txt

# In production you can just run the image,
# when testing a volume gets mounted here.
EXPOSE 5000
WORKDIR /srv
COPY hello.py start_app.py

ENV FLASK_APP "start_app"
ENV FLASK_DEBUG "1"
ENV PYTHONPATH /srv

ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
