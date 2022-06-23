#!/usr/bin/env python3
""" Get the total size in human readable format for a RDS database logs.

        For usage type: rds-logs-size.py -h/--help

   By Carlos Bustillo <https://linkedin.com/in/carlosbustillordguez/>
"""
import argparse
import sys
import textwrap

import boto3
from botocore.exceptions import ProfileNotFound


def init_aws_clients(options):
    """ Initialize the AWS clients.

        Args:
            options: the script arguments.
    """
    # AWS Profile to perform the operations
    aws_profile = options.profile
    aws_region_arg = options.region

    # Global variables
    global rds
    global aws_region

    # Configured the session for the boto3 client
    if aws_profile and aws_region_arg:
        try:
            session = boto3.Session(
                profile_name=aws_profile,
                region_name=aws_region_arg,
            )
        except ProfileNotFound as e:
            print(f"{sys.argv[0]} error: " + str(e))
            sys.exit(1)
    elif aws_profile:
        try:
            session = boto3.Session(profile_name=aws_profile)
        except ProfileNotFound as e:
            print(f"{sys.argv[0]} error: " + str(e))
            sys.exit(1)
    elif aws_region_arg:
        session = boto3.Session(region_name=aws_region_arg)
        if aws_region_arg not in session.get_available_regions('rds'):
            print(f"{sys.argv[0]} error: the specified region {aws_region_arg} is not a valid AWS region")
            sys.exit(1)
    else:
        session = boto3.Session()

    # Create the RDS client
    rds = session.client('rds')

    # Get the AWS region for the current session
    aws_region = session.region_name


def parse_options(args=sys.argv[1:]):
    """ Parse the script options.

        Args:
            args: the script arguments.
    """

    # Create the top-level parser
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Get the total size in human readable format for a RDS database logs.",
        epilog=textwrap.dedent(f'''\
            Usage samples:
            --------------
                To list the available RDS instances ID:
                    {sys.argv[0]} --list-instances

                To get the total size of RDS database logs:
                    {sys.argv[0]} --instance-id <INSTANCE_ID>
            '''),
    )

    # Global options
    parser.add_argument("-p", "--profile", help="a valid AWS profile name to perform the import or export operation")
    parser.add_argument("-r", "--region", help="a valid AWS region to perform the tasks")

    # Mutually exclusive options - one is required
    me_options = parser.add_mutually_exclusive_group(required=True)
    me_options.add_argument("-i", "--instance-id", help="the RDS instance ID to get the database logs size")
    me_options.add_argument("-l", "--list-instances", help="list the RDS instances", action="store_true")

    # Print usage and exit if not arguments are supplied
    if not args:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Parse the args
    options = parser.parse_args(args)

    # Return the parsed args
    return options


def get_rds_instances():
    """ Get the available RDS instances in the region.

        Args: None.
    """

    try:
        response = rds.describe_db_instances()
        if response['DBInstances']:
            print("RDS Instance ID:")
            print("----------------")
            for instance in response['DBInstances']:
                print(instance['DBInstanceIdentifier'])
        else:
            print("No RDS instances found!!")
    except rds.exceptions.DBInstanceNotFoundFault as e:
        print(e)


def get_rds_log_size(options):
    """ Get the total size in GB for the database logs.

        Args:
            options: parsed command line options.
    """

    # RDS instance ID
    db_instance_id = options.instance_id

    # Get the instance log files
    try:
        response = rds.describe_db_log_files(DBInstanceIdentifier=db_instance_id)
    except rds.exceptions.DBInstanceNotFoundFault:
        print(f"The database instance {db_instance_id} not found!!")
    else:
        # In Bytes
        total_log_size = 0

        # Sum the logs size
        for i in range(len(response['DescribeDBLogFiles'])):
            total_log_size = total_log_size + int(response['DescribeDBLogFiles'][i]['Size'])

        # Convert the logs total size in human readable format
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if total_log_size < 1024 or unit == 'PB':
                break
            total_log_size /= 1024
        print(f"The total logs size is {round(total_log_size, 2)} {unit}")


def main():
    """ Main function.

        Args:
          None.
    """

    # Parse the args
    options = parse_options(sys.argv[1:])

    # Initialize the AWS clients
    init_aws_clients(options)

    # Script actions
    if options.list_instances:
        # Get the available RDS instances
        get_rds_instances()
    else:
        # Get the total size in GB for the database logs
        get_rds_log_size(options)


if __name__ == "__main__":
    main()
