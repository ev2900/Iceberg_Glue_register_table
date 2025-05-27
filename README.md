# Iceberg Glue - register_table

<img width="275" alt="map-user" src="https://img.shields.io/badge/cloudformation template deployments-94-blue"> <img width="85" alt="map-user" src="https://img.shields.io/badge/views-1131-green"> <img width="125" alt="map-user" src="https://img.shields.io/badge/unique visits-368-green">

The Apache Iceberg ```register_table``` can be used to register Iceberg metadata file to a new data catalog table. This functionality is especially useful in data catalog migrations.

> [!CAUTION]
> ```register_table``` will **NOT** change the S3 locations, manifest-list locations etc. in any of the Iceberg metadata files. It will not change any of the S3 file paths in the metadata.json files or any of the avro files in the metadata directoy of an Iceberg table.
>
> If you want to change the S3 locations in the metadata.json and avro metadata files before running ```register_table``` you can consider using the script in the [Iceberg_update_metadata_script](https://github.com/ev2900/Iceberg_update_metadata_script/tree/main) repository to update these.

The use case for ```register_table``` is your Iceberg datafiles and metadata files are **staying the same S3 location** but you want to register them as a new data catalog table.

## Example using AWS Glue and Glue Data Catalog

Launch the CloudFormation stack below to walk through an example. In the example you will creating an Iceberg table in the Glue Data Catalog database ```iceberg``` via. a Glue job. Then you will use another Glue job to register the table you created with a different Glue Data Catalog Database ```icebergregister```

### Launch the CloudFormation stack

Click the button below to launch a CloudFormation stack. The stack will deploy everything we need including Glue jobs, Glue Data Catalog databases, S3 buckets etc.

> [!NOTE]
> The Glue jobs this cloudformation stack deploys uses Iceberg version 1.6.1

[![Launch CloudFormation Stack](https://sharkech-public.s3.amazonaws.com/misc-public/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=iceberg&templateURL=https://sharkech-public.s3.amazonaws.com/misc-public/glue_iceberg_register_table.yaml)

### Run the Glue job to Create Iceberg table

Open the [Glue Console](https://us-east-1.console.aws.amazon.com/gluestudio/home). Select the ETL jobs section and click on run the *0 Create Iceberg Table* and then *Run job*

<img width="700" alt="quick_setup" src="https://github.com/ev2900/Iceberg_Glue_register_table/blob/main/REAME/run_glue_job_1.PNG">

This will create a table in Glue Data Catalog named *iceberg*

<img width="700" alt="quick_setup" src="https://github.com/ev2900/Iceberg_Glue_register_table/blob/main/REAME/glue_table_1.PNG">

## Update and run the Glue job to register the Iceberg table

Open the [Glue Console](https://us-east-1.console.aws.amazon.com/gluestudio/home). Select the ETL jobs section and click on edit

<img width="700" alt="quick_setup" src="https://github.com/ev2900/Iceberg_Glue_register_table/blob/main/REAME/edit_job_1.png">

In the Glue script we need to edit the query

```
CALL glue_catalog.system.register_table(
  table => 'icebergregister.registersampledataicebergtable',
  metadata_file => 's3://<bucket-name>/iceberg/iceberg.db/sampledataicebergtable/metadata/<most-recent-snapshot-file>.metadata.json'
```

Specifically you need to replace the ```<bucket-name>``` and ```<most-recent-snapshot-file>``` file name. You want the ```register_table```, ```metadata_file``` to reference the most recent *.metadata.json* file. This *.metadata.json* files was created when you ran the *0_create_iceberg_table.py* job to create the initial Iceberg table. You can find the name of the S3 bucket and the name of the most recent snapshot file by navigating through the [S3 console](https://us-east-1.console.aws.amazon.com/s3/home)

Once you update the Glue script **Save** and **Run** the job.

After running the Glue job. The Glue Data Catalog will have a new table *registersampledataicebergtable* created in the *icebergregister* database

<img width="700" alt="quick_setup" src="https://github.com/ev2900/Iceberg_Glue_register_table/blob/main/REAME/registered_table.PNG">
