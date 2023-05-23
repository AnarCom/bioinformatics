FROM apache/airflow:latest
USER root
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y freebayes minimap2 fastqc bwa samtools

ADD process.sh /usr/bin

RUN mkdir /host 
WORKDIR /host

USER 50000
RUN AIRFLOW__CORE__LOAD_EXAMPLES=False airflow db init && airflow users  create --role Admin --username q --email q --firstname admin --lastname admin --password q

ADD dags /opt/airflow/dags

CMD [ "standalone" ]