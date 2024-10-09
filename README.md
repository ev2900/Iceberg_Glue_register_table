# Iceberg Glue - register_table

<img width="275" alt="map-user" src="https://img.shields.io/badge/cloudformation template deployments-23-blue"> <img width="85" alt="map-user" src="https://img.shields.io/badge/views-116-green"> <img width="125" alt="map-user" src="https://img.shields.io/badge/unique visits-012-green">

The Apache Iceberg ```register_table``` can be used to register Iceberg metadata file to a new data catalog table. This functionality is especially useful in data catalog migrations.

> [!CAUTION]
> ```register_table``` will **NOT** change the S3 locations, manifest-list locations etc. in any of the Iceberg metadata files. It will not change any of the S3 file paths in the metadata.json files or any of the avro files in the metadata directoy of an Iceberg table

The use case for ```register_table``` is your Iceberg datafiles and metadata files are **staying the same S3 location** but you want to register them as a new data catalog table.

## Example using AWS Glue and Glue Data Catalog

Launch the CloudFormation stack below to walk through an example. In the example you will creating an Iceberg table in the Glue Data Catalog database ```iceberg``` via. a Glue job. Then you will use another Glue job to regsiter the table you created with a different Glue Data Catalog Database ```icebergregister```

### Lunch the CloudFormation stack

[![Launch CloudFormation Stack](https://sharkech-public.s3.amazonaws.com/misc-public/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=iceberg&templateURL=https://sharkech-public.s3.amazonaws.com/misc-public/glue_iceberg_register_table.yaml)

