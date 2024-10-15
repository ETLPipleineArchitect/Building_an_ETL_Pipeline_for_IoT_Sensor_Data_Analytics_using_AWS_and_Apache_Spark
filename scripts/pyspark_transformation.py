from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType

# Initialize Spark Session
spark = SparkSession.builder.appName("IoTSensorDataAnalytics").getOrCreate()

schema = StructType([
    StructField("sensor_id", StringType(), True),
    StructField("timestamp", LongType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("humidity", DoubleType(), True),
    StructField("pressure", DoubleType(), True)
])

raw_df = spark.read.json("s3://your-bucket/iot_data/raw/*", schema=schema)

# Data Cleaning and Transformation
cleaned_df = raw_df.dropna()

# Write Processed Data to S3 in Parquet Format
cleaned_df.write.parquet("s3://your-bucket/iot_data/processed/", mode='append')
