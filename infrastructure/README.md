Set up AWS infrastructure for the sessions.

## Tools

### NodeJS

CDK needs NodeJS to run. Installation instructions [here](https://nodejs.org/en/download/package-manager/).

To install latest via snap on Ubuntu: `sudo snap install node --classic`

### aws-cli

Will need AWS creds. AWS CLI v2 is not generally available in package repositories :(

See [here](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html#cliv2-linux-install) for instructions.

[../install_aws_cli.sh](../install_aws_cli.sh) is script to install the AWS CLI v2 on Linux using the method outlined in the above documentation.

Configuration: see [instructions](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html).

### aws-sdk

To avoid global installation:

`npx aws-cdk`

