import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from awsglue.context import GlueContext

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

source_data = glueContext.create_dynamic_frame.from_catalog(database="sales_db", table_name="sales_data")

from pyspark.sql.functions import col, sum

transformed_data = source_data.toDF() \
    .groupBy("Product") \
    .agg(sum("Revenue").alias("TotalRevenue"))

transformed_dynamic_frame = DynamicFrame.fromDF(transformed_data, glueContext, "transformed_dynamic_frame")

glueContext.write_dynamic_frame.from_catalog(dynamic_frame=transformed_dynamic_frame, database="sales_db", table_name="transformed_data")
