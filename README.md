# healthfinch's fork of `dbsnap`

Forked from this: https://github.com/remind101/dbsnap
into this:        https://github.com/healthfinch/dbsnap

## Deploy:
1. Make changes in dbsnap/dbsnap_verify/\*.py
2. `make build-lambda` *(creates a new ZIP file in artifacts/)*
3. Rename your ZIP file to be `lambda-dbsnap-YYYY-MM-DDx.zip`, where `x` is a letter for version tracking if you don't want to overwrite what we already have
4. ```aws s3 cp artifacts/<renamedFile>.zip s3://healthfinch-running-app-files/rds-snapshot/```
5. Move over to the `rds-snapshot` repo
6. Edit filename in parameters file `rds-snapshot/production.json` and save
7. `aws cloudformation update-stack --stack-name rds-snapshot --template-body file://./deploy/cloudformation.yml --capabilities CAPABILITY_IAM --parameters file://./deploy/production.json`
    This will redeploy, and your Lambda in the stack will pull updated code from the S3 file


# Original `dbsnap`

Here at `Remind <https://www.remind.com>`_ we maintain a set of tools and
Python libraries to copy and verify AWS RDS DB Instance and Cluster Snapshots.

``dbsnap-copy``:
 AWS RDS allows a maximum of 35 "automatic" daily snapshots.
 We wrote this tool to copy "automatic" snapshots as "manual" snapshots.
 We also use this tool to increase our disaster recovery fitness by
 copying snapshots to remote regions.

For more details read: `dbsnap_copy/README.rst <https://github.com/remind101/dbsnap-verify/blob/master/dbsnap_copy/README.rst>`_

``dbsnap-verify``:
 We use this tool to automate testing RDS snapshot restore process.
 This gives us confidence that we have the ability to recover from
 our database backups in case of a disaster.

For more details read: `dbsnap_verify/README.rst <https://github.com/remind101/dbsnap-verify/blob/master/dbsnap_verify/README.rst>`_

