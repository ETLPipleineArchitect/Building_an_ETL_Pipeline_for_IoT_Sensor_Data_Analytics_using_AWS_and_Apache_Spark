## **Project Overview**

**Title:** **Building an ETL Pipeline for IoT Sensor Data Analytics using AWS and Apache Spark**

**Objective:** Develop an end-to-end ETL pipeline that ingests, processes, and analyzes IoT sensor data (e.g., temperature, humidity, pressure) to extract insights and enable real-time monitoring. This project involves data ingestion, cleaning, transformation, and analysis using AWS services and Apache Spark tools.

**Technologies Used:**

- **AWS Services:** S3, Kinesis Data Streams, Kinesis Data Firehose, Lambda, EMR, AWS Glue
- **Programming Languages:** Python, SQL
- **Big Data Technologies:** Apache Spark, SparkSQL, PySpark
- **Others:** Regular Expressions for data parsing, Data Visualization tools

---

## **Project Architecture**

1. **Data Ingestion:**
   - Simulate IoT sensor data using a Python script.
   - Stream data into **AWS Kinesis Data Streams**.

2. **Data Processing:**
   - Use **AWS Lambda** functions to process incoming data from Kinesis Streams.
   - Perform data cleaning and transformation using **Regular Expressions** and **PySpark**.

3. **Data Transformation:**
   - Use **Apache Spark** on **AWS EMR** to perform large-scale data transformations.
   - Aggregate data to compute metrics like average temperature, humidity, etc.

4. **Data Storage:**
   - Store raw and processed data in **Amazon S3**.
   - Use **Parquet** format for processed data for efficient querying.

5. **Data Analysis:**
   - Use **SparkSQL** to query processed data.
   - Detect anomalies, identify trends, and generate insights.

6. **Visualization:**
   - Use **Jupyter Notebooks** on EMR or **Amazon QuickSight** for data visualization and reporting.

---

## **Step-by-Step Implementation Guide**

### **1. Setting Up AWS Resources**

- **Create an S3 Bucket:**
  - Store raw sensor data, processed data, and analysis outputs.

- **Set Up IAM Roles:**
  - Configure roles with necessary permissions for Kinesis, Lambda, EMR, and S3.

- **Set Up AWS Kinesis Data Streams:**
  - Create a Kinesis Data Stream to ingest sensor data.

### **2. Simulating IoT Sensor Data**

- **Create a Python Script to Simulate Sensor Data:**

  ```python
  import json
  import time
  import random
  import boto3

  kinesis_client = boto3.client('kinesis', region_name='YOUR_REGION')

  def generate_sensor_data():
      sensor_data = {
          'sensor_id': random.randint(1, 100),
          'timestamp': int(time.time() * 1000),
          'temperature': round(random.uniform(20.0, 30.0), 2),
          'humidity': round(random.uniform(30.0, 70.0), 2),
          'pressure': round(random.uniform(1.0, 1.5), 2)
      }
      return sensor_data

  while True:
      data = generate_sensor_data()
      kinesis_client.put_record(
          StreamName='YOUR_KINESIS_STREAM_NAME',
          Data=json.dumps(data),
          PartitionKey=str(data['sensor_id'])
      )
      print(f"Sent data: {data}")
      time.sleep(1)
  ```

- **Run the Script:**
  - Ensure the script runs continuously to simulate real-time data streaming.

### **3. Data Ingestion with AWS Kinesis**

- **AWS Kinesis Data Streams:**
  - Collect data from the simulated IoT sensors.

- **Set Up AWS Kinesis Data Firehose (Optional):**
  - Deliver streaming data to S3 in near real-time.

### **4. Data Processing with AWS Lambda and PySpark**

#### **a. AWS Lambda Function for Preprocessing**

- **Write a Lambda Function:**
  - Use Python to preprocess streaming data.
  - **Use Regular Expressions** to validate and clean the data.

  ```python
  import json
  import re

  def lambda_handler(event, context):
      for record in event['Records']:
          payload = base64.b64decode(record['kinesis']['data'])
          data = json.loads(payload)
          cleaned_data = preprocess_data(data)
          if cleaned_data:
              # Send cleaned data to another Kinesis Stream or store in S3
              pass
      return 'Processed'

  def preprocess_data(data):
      # Validate data using regex
      sensor_id_pattern = re.compile(r'^\d+$')
      if not sensor_id_pattern.match(str(data.get('sensor_id', ''))):
          return None
      # Additional validation and cleaning
      return data
  ```

#### **b. Setting Up an EMR Cluster for Data Transformation**

- **Launch an EMR Cluster:**
  - Enable applications like Hadoop and Spark.
  - Configure the cluster with appropriate instance types.

#### **c. Writing the PySpark Script for Data Transformation**

- **Import Necessary Libraries:**

  ```python
  from pyspark.sql import SparkSession
  from pyspark.sql.functions import from_json, col, window
  from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType
  ```

- **Initialize Spark Session:**

  ```python
  spark = SparkSession.builder.appName("IoTSensorDataAnalytics").getOrCreate()
  ```

- **Define Schema for Sensor Data:**

  ```python
  schema = StructType([
      StructField("sensor_id", StringType(), True),
      StructField("timestamp", LongType(), True),
      StructField("temperature", DoubleType(), True),
      StructField("humidity", DoubleType(), True),
      StructField("pressure", DoubleType(), True)
  ])
  ```

- **Read Data from S3:**

  ```python
  raw_df = spark.read.json("s3://your-bucket/iot_data/raw/*", schema=schema)
  ```

- **Data Cleaning and Transformation:**

  - **Handle Missing Values:**

    ```python
    cleaned_df = raw_df.dropna()
    ```

  - **Convert Timestamp to DateTime:**

    ```python
    from pyspark.sql.functions import from_unixtime

    cleaned_df = cleaned_df.withColumn('datetime', from_unixtime(col('timestamp') / 1000))
    ```

- **Aggregate Data:**

  ```python
  aggregated_df = cleaned_df.groupBy('sensor_id').agg({
      'temperature': 'avg',
      'humidity': 'avg',
      'pressure': 'avg'
  }).withColumnRenamed('avg(temperature)', 'avg_temperature') \
    .withColumnRenamed('avg(humidity)', 'avg_humidity') \
    .withColumnRenamed('avg(pressure)', 'avg_pressure')
  ```

- **Data Storage:**

  - **Write Processed Data to S3 in Parquet Format:**

    ```python
    cleaned_df.write.parquet("s3://your-bucket/iot_data/processed/", mode='append')
    aggregated_df.write.parquet("s3://your-bucket/iot_data/aggregated/", mode='overwrite')
    ```

### **5. Data Analysis with SparkSQL**

- **Register DataFrames as Temporary Views:**

  ```python
  cleaned_df.createOrReplaceTempView("sensor_data")
  ```

- **Example Queries:**

  - **Identify Sensors with Abnormal Temperature Readings:**

    ```python
    abnormal_temps = spark.sql("""
      SELECT sensor_id, temperature, datetime
      FROM sensor_data
      WHERE temperature > 28.0
    """)
    abnormal_temps.show()
    ```

  - **Calculate Average Metrics per Sensor:**

    ```python
    avg_metrics = spark.sql("""
      SELECT sensor_id,
             AVG(temperature) as avg_temp,
             AVG(humidity) as avg_humidity,
             AVG(pressure) as avg_pressure
      FROM sensor_data
      GROUP BY sensor_id
    """)
    avg_metrics.show()
    ```

- **Save Query Results:**

  ```python
  abnormal_temps.write.csv("s3://your-bucket/iot_data/output/abnormal_temps.csv", mode='overwrite')
  avg_metrics.write.csv("s3://your-bucket/iot_data/output/avg_metrics.csv", mode='overwrite')
  ```

### **6. Visualization**

#### **a. Using Jupyter Notebooks on EMR**

- **Install Jupyter Notebook:**
  - Use bootstrap actions when launching EMR or install manually.

- **Visualize Data with Matplotlib or Seaborn:**

  ```python
  import pandas as pd
  import matplotlib.pyplot as plt
  import seaborn as sns

  # Convert Spark DataFrame to Pandas DataFrame
  metrics_pd = avg_metrics.toPandas()

  # Plot Average Temperature per Sensor
  plt.figure(figsize=(12, 6))
  sns.barplot(data=metrics_pd, x='sensor_id', y='avg_temp')
  plt.title('Average Temperature per Sensor')
  plt.xlabel('Sensor ID')
  plt.ylabel('Average Temperature (°C)')
  plt.show()
  ```

#### **b. Using Amazon QuickSight**

- **Set Up Data Source:**
  - Connect QuickSight to your S3 bucket containing the processed data.

- **Create Dashboards:**
  - Visualize sensor metrics, trends over time, and anomaly detection.

---

## **Project Documentation**

- **README.md:**

  - **Project Title:** Building an ETL Pipeline for IoT Sensor Data Analytics using AWS and Apache Spark

  - **Description:**
    - An end-to-end data engineering project that simulates IoT sensor data and processes it using AWS services and Apache Spark to extract meaningful insights.

  - **Contents:**
    - **Introduction**
    - **Project Architecture**
    - **Technologies Used**
    - **Dataset Information**
    - **Setup Instructions**
      - Prerequisites
      - AWS Configuration
    - **Running the Project**
    - **Data Processing Steps**
    - **Data Analysis and Results**
    - **Visualization**
    - **Conclusion**

  - **License and Contribution Guidelines**

- **Code Organization:**

  ```
  ├── README.md
  ├── scripts
  │   ├── data_visualization.py
  │   ├── lambda_preprocessing.py
  │   ├── pyspark_transformation.py
  │   ├── simulate_sensor_data.py
  │   ├── spark_analysis.py  
  ├── notebooks
  │   └── visualization.ipynb
  └── data
      └── sample_sensor_data.json
  ```

- **Comments and Docstrings:**
  - Include detailed docstrings for all functions and classes.
  - Comment on complex code blocks to explain the logic.

---

## **Best Practices**

- **Use Version Control:**

  - Initialize a Git repository and commit changes regularly.

    ```
    git init
    git add .
    git commit -m "Initial commit with project structure and documentation"
    ```

- **Handle Exceptions:**

  - Add error handling in Python scripts and Lambda functions.
  - Use logging to capture and debug issues.

- **Security:**

  - **Do not expose AWS credentials** in your code.
  - Use IAM roles for permissions.
  - Apply proper encryption and access policies for S3 buckets.

- **Optimization:**

  - **Efficient Data Processing:**
    - Use appropriate Spark configurations.
    - Partition data based on sensor IDs or timestamps.

  - **Resource Management:**
    - Monitor EMR cluster performance.
    - Scale the cluster based on workload.

- **Cleanup Resources:**

  - Terminate EMR clusters and stop Lambda functions when not in use.
  - Delete S3 test data if not needed.

---

## **Demonstrating Skills**

- **Regular Expressions:**
  - Validate and clean sensor data fields.
  - Parse log messages if necessary.

- **SQL and SparkSQL:**
  - Perform complex queries to analyze sensor data.
  - Use window functions for time-based aggregations.

- **Python and PySpark:**
  - Simulate real-time data generation.
  - Write efficient PySpark code for data transformations.

- **Data Engineering Concepts:**
  - Implement streaming data ingestion.
  - Design an ETL pipeline for real-time and batch processing.

- **Big Data Handling:**
  - Process and analyze large volumes of sensor data efficiently.
  - Optimize Spark jobs for performance.

---

## **Additional Enhancements**

- **Implement Unit Tests:**

  - Use `pytest` for testing data processing functions and Lambda code.

    ```python
    def test_preprocess_data():
        sample_data = {'sensor_id': '101', 'temperature': 25.6}
        assert preprocess_data(sample_data) == sample_data
    ```

- **Continuous Integration:**

  - Set up GitHub Actions to automate testing and code quality checks.

- **Containerization:**

  - Use Docker to containerize data simulation and processing scripts.

    ```dockerfile
    FROM python:3.8-slim

    RUN pip install boto3

    COPY simulate_sensor_data.py /app/
    WORKDIR /app

    CMD ["python", "simulate_sensor_data.py"]
    ```

- **Machine Learning Integration:**

  - Implement anomaly detection using machine learning algorithms.

    ```python
    from pyspark.ml.clustering import KMeans
    from pyspark.ml.feature import VectorAssembler

    assembler = VectorAssembler(inputCols=['temperature', 'humidity', 'pressure'], outputCol='features')
    feature_df = assembler.transform(cleaned_df)

    kmeans = KMeans().setK(2).setSeed(1)
    model = kmeans.fit(feature_df.select('features'))

    transformed_df = model.transform(feature_df)
    transformed_df.select('sensor_id', 'features', 'prediction').show()
    ```

- **Streaming Analytics:**

  - Use **Spark Structured Streaming** for real-time processing.

    ```python
    stream_df = spark \
      .readStream \
      .format("kinesis") \
      .option("streamName", "YOUR_KINESIS_STREAM_NAME") \
      .option("region", "YOUR_REGION") \
      .load()

    processed_stream = stream_df.selectExpr("CAST(data AS STRING)") \
      .select(from_json(col("data"), schema).alias("data")) \
      .select("data.*")

    query = processed_stream.writeStream \
      .outputMode("append") \
      .format("parquet") \
      .option("path", "s3://your-bucket/iot_data/streaming/") \
      .option("checkpointLocation", "s3://your-bucket/iot_data/checkpoints/") \
      .start()

    query.awaitTermination()
    ```

- **Alerting and Notifications:**

  - Integrate AWS SNS to send alerts based on certain conditions, e.g., abnormal sensor readings.

- **Data Lake Formation:**

  - Use AWS Lake Formation to manage data securely.
