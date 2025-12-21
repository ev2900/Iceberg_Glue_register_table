# Iceberg Glue - register_table

<img width="275" alt="map-user" src="https://img.shields.io/badge/cloudformation template deployments-151-blue"> <img width="85" alt="map-user" src="https://img.shields.io/badge/views-1707-green"> <img width="125" alt="map-user" src="https://img.shields.io/badge/unique visits-592-green">

The Apache Iceberg ```register_table``` can be used to register Iceberg metadata file to a new data catalog table. This functionality is especially useful in data catalog migrations.

> [!CAUTION]
> ```register_table``` will **NOT** change the S3 absolute paths in the Iceberg metadata files.
>
> If you want to change the S3 absolute paths bc. you are migrating the table storage (not just the catalog) you need to first use the ```rewrite_table_path``` procedure to update the S3 absolute paths in the metadata files. The documentation for this procedure is [HERE](https://iceberg.apache.org/docs/1.9.0/spark-procedures/#rewrite_table_path).
>
> After you run ```rewrite_table_path``` you can use ```register_table``` referencing the updated metadata.
>
> This is only applicable if you are moving the Iceberg table to a different S3 bucket or prefix. If you are leaving the S3 location the same and just migrating it to a new data catalog entry you skip the  ```rewrite_table_path``` procedure and go straight to ```register_table```

The use case for ```register_table``` is your Iceberg datafiles and metadata files are **staying the same S3 location** but you want to register them as a new data catalog table.

## Example using AWS Glue and Glue Data Catalog

Launch the CloudFormation stack below to walk through an example. In the example you will creating an Iceberg table in the Glue Data Catalog database ```iceberg``` via. a Glue job. Then you will use another Glue job to register the table you created with a different Glue Data Catalog Database ```icebergregister```

### Launch the CloudFormation stack

Click the button below to launch a CloudFormation stack. The stack will deploy everything we need including Glue jobs, Glue Data Catalog databases, S3 buckets etc.

> [!WARNING]
> The CloudFormation stack creates IAM role(s) that have ADMIN permissions. This is not appropriate for production deployments. Scope these roles down before using this CloudFormation in production.

> [!NOTE]
> The Glue jobs this cloudformation stack deploys uses Iceberg version 1.10.0

[![Launch CloudFormation Stack](https://sharkech-public.s3.amazonaws.com/misc-public/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=iceberg-register-table&templateURL=https://sharkech-public.s3.amazonaws.com/misc-public/glue_iceberg_register_table.yaml)

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
