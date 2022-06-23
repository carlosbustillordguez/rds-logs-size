# RDS Logs Size

Get the total size in human readable format for a RDS database logs.

**Table of Contents:**

- [RDS Logs Size](#rds-logs-size)
  - [Requirements](#requirements)
  - [How to use the tool](#how-to-use-the-tool)
  - [License](#license)
  - [Author Information](#author-information)

## Requirements

- Python version 3+.
- For Python requirements see the `requirements.txt` file.
- To get the RDS logs information the following IAM permission is required:
  - `rds:DescribeDBInstances`
  - `rds:DescribeDBLogFiles`

## How to use the tool

1- Install the Python requirements:

```bash
pip3 install -r requirements.txt
```

2- List the available RDS instances or get the total logs size for an RDS instance:

```bash
# To list the available RDS instances ID:
rds-logs-size.py -l

# To get the total logs size for the RDS instance ID **myinstance**:
rds-logs-size.py -i myinstance
```

**NOTES**:

- You can set the `AWS_PROFILE` or `AWS_DEFAULT_PROFILE` before execute this script and ommit the optional parameter `-p/--profile`.
- To see all available arguments, execute the script with arguments or with `-h | --help`.

## License

MIT

## Author Information

By: [Carlos M Bustillo Rdguez](https://linkedin.com/in/carlosbustillordguez/)
