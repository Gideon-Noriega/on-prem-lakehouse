FROM apache/spark:3.5.3

USER root

# Add Iceberg, Hive Metastore, and S3 JARs
RUN curl -L -o /opt/spark/jars/iceberg-spark-runtime-3.5_2.12-1.7.1.jar \
    https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.7.1/iceberg-spark-runtime-3.5_2.12-1.7.1.jar && \
    curl -L -o /opt/spark/jars/iceberg-aws-bundle-1.7.1.jar \
    https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-aws-bundle/1.7.1/iceberg-aws-bundle-1.7.1.jar && \
    curl -L -o /opt/spark/jars/hadoop-aws-3.3.4.jar \
    https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar && \
    curl -L -o /opt/spark/jars/aws-java-sdk-bundle-1.12.367.jar \
    https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.367/aws-java-sdk-bundle-1.12.367.jar

USER spark
