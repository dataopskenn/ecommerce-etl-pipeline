# Configuration Files

There are three YAML files contained in this folder, each holding the configuration parameters for different phases of this project;

- aws_keys.yml
- config.yml
- new_config.yml


## ```aws_keys.yml```

This file contains two parameters;
```access_key```: which is the AWS account access key.
```secret_key```: which is the AWS account secret key.


## ```config.yml```

After the AWS PostgreSQL RDS instance has been created, the parameters in this file are used to create the database connection needed to execute the SQL queries for data transformation. Although, the target of this connection is the same database for the schema that has been created, the connection is targetted at the default Postgres "public" schema, which then opens the database for the app.py file to execute the ETL queries.

There are essentially five (5) parameters contained in this file,
- ```host```: is the endpoint of the AWS Postgres RDS instance, usually in the format `db_name.xxxxxxxxxxxx.availability_zone.rds.amazonaws.com`. This is where the database is hosted. This is also the same host needed to connect to `PgAdmin4`.
- ```db_name```: is the name of the default database in Postgres. This is the `public` database.
- ```user```: is the username specified for the database instance.
- ```password```: is the password specified for the database instance. This will also be needed to connect to `PgAdmin4`.
- ```port```: is the port number of the database instance. By default, this is `5432`.


## ```new_config.yml```

This file is essentially the same information, the only difference being that the target database is the same as the database we created from our terraform IaC.

There are essentially five (5) parameters contained in this file,
- ```host```: is the endpoint of the AWS Postgres RDS instance, usually in the format `db_name.xxxxxxxxxxxx.availability_zone.rds.amazonaws.com`. This is where the database is hosted. This is also the same host needed to connect to `PgAdmin4`.
- ```db_name```: is the name of the database, the same way it was declared while the terraform infrastructure was being built.
- ```user```: is the username specified for the database instance.
- ```password```: is the password specified for the database instance. This will also be needed to connect to `PgAdmin4`.
- ```port```: is the port number of the database instance. By default, this is `5432`.

All of the values needed to input into this file can be printed as a terraform output. They will be printed out in the `Terminal` console (this is not recommended, it is not safe), and also in `Terraform Cloud` for safe keeping (assuming terraform has been setup and connected to the workspace).