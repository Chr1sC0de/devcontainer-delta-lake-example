# Command to run

## Install

poetry install -C=library

## Running tests

pytest --config-file library/pyproject.toml

## Other commands

create a bind mount to the current folder

```powershell
docker run -d -v .:/app --name
```

start the moto host

```bash
moto_server -H 127.0.0.1 -p 5000
```

start the spark server

```bash
$SPARK_HOME/sbin/start-master.sh
$SPARK_HOME/sbin/start-worker.sh spark://32d5268f3b97:7077

$SPARK_HOME/sbin/stop-master.sh
$SPARK_HOME/sbin/stop-worker.sh
```

submit an application

```bash
$SPARK_HOME/bin/spark-submit  \
--master spark://32d5268f3b97:7077 \
--packages "org.apache.hadoop:hadoop-aws:3.3.2","io.delta:delta-core_2.12:2.4.0" \
--conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
--conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
--conf spark.hadoop.fs.s3.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
--conf spark.hadoop.fs.s3a.access.key="testing" \
--conf spark.hadoop.fs.s3a.secret.key="testing" \
--conf spark.hadoop.com.amazonaws.services.s3.enableV4=true \
--conf spark.hadoop.fs.s3a.endpoint="http://127.0.0.1:5000" \
--conf spark.sql.catalogImplementation=hive \
./app/mock-environment.py
```

start the required pyspark instance

```bash
pyspark \
--master spark://32d5268f3b97:7077 \
--packages "org.apache.hadoop:hadoop-aws:3.3.2","io.delta:delta-core_2.12:2.4.0" \
--conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
--conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" \
--conf "spark.executor.extraJavaOptions=com.amazonaws.services.s3.enableV4=true" \
--conf "spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem" \
--conf "spark.hadoop.fs.s3.impl=org.apache.hadoop.fs.s3a.S3AFileSystem" \
--conf "spark.hadoop.fs.s3a.access.key=testing" \
--conf "spark.hadoop.fs.s3a.secret.key=testing" \
--conf "spark.hadoop.fs.s3a.endpoint=http://127.0.0.1:5000" \
--name "Mocked Environment"
app mock-environment.py
```

start a thrift server

```bash
$SPARK_HOME/sbin/start-thriftserver.sh \
--master spark://32d5268f3b97:7077 \
--packages "org.apache.hadoop:hadoop-aws:3.3.2","io.delta:delta-core_2.12:2.4.0" \
--conf spark.sql.catalogImplementation=hive \
--conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
--conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
--conf spark.hadoop.fs.s3.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
--conf spark.hadoop.fs.s3a.access.key="testing" \
--conf spark.hadoop.fs.s3a.secret.key="testing" \
--conf spark.hadoop.com.amazonaws.services.s3.enableV4=true \
--conf spark.hadoop.fs.s3a.endpoint="http://127.0.0.1:5000" \

$SPARK_HOME/sbin/stop-thriftserver.sh
$SPARK_HOME/bin/beeline -u jdbc:hive2://127.0.0.1:10000
```

if get an error relating to delta not found need to copy delta jars to "$SPARK_HOME/jars"

To run build and run the docker container indefinitely as a dev container

```bash
docker run -d your-image-name 'tail -f /dev/null'
```
