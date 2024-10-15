from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder.appName("IoTSensorDataAnalytics").getOrCreate()

# Load Processed Data
processed_data_path = "s3://your-bucket/iot_data/processed/"
data_df = spark.read.parquet(processed_data_path)

data_df.createOrReplaceTempView("sensor_data")

abnormal_temps = spark.sql("""
  SELECT sensor_id, temperature, timestamp
  FROM sensor_data
  WHERE temperature > 28.0
""")
abnormal_temps.show()

abnormal_temps.write.csv("s3://your-bucket/iot_data/output/abnormal_temps.csv", mode='overwrite')
