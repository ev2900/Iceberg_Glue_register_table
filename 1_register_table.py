from pyspark.sql import SparkSession

# Import additional libraries
from pyspark.sql.functions import col, to_timestamp, monotonically_increasing_id, to_date, when
from pyspark.sql.types import *
from datetime import datetime
import sys
from awsglue.utils import getResolvedOptions

# Create an array of the job parameters
args = getResolvedOptions(sys.argv, ['s3_bucket_name'])

# Initialize a SparkSession
spark = SparkSession.builder \
    .appName("IcebergIntegration") \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.glue_catalog", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.glue_catalog.warehouse", "s3://" + args['s3_bucket_name'] + "/iceberg/") \
    .config("spark.sql.catalog.glue_catalog.catalog-impl", "org.apache.iceberg.aws.glue.GlueCatalog") \
    .config("spark.sql.catalog.glue_catalog.io-impl", "org.apache.iceberg.aws.s3.S3FileIO") \
    .getOrCreate()

query = f"""
CALL glue_catalog.system.register_table(
  table => 'icebergregister.registersampledataicebergtable',
  metadata_file => 's3://<bucket-name>/iceberg/iceberg.db/sampledataicebergtable/<most-recent-snapshot-file>.metadata.json')
"""

spark.sql(query)
