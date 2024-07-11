ARG FLINK_VERSION=1.19.1

FROM flink:${FLINK_VERSION}

# install python3, pip3, and the JDK
RUN \
  apt-get update -y && \
  apt-get install -y python3 python3-pip python3-dev git openjdk-11-jdk && \
  rm -rf /var/lib/apt/lists/* && \
  ln -s /usr/bin/python3 /usr/bin/python
ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-arm64/"
ENV PATH="${JAVA_HOME}:${PATH}"

# install PyFlink and Ibis
ARG FLINK_VERSION
RUN pip3 install apache-flink==${FLINK_VERSION} ibis-framework
