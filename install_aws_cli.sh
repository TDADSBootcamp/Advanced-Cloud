#!/bin/bash

set -euo pipefail

AWS_CLI_ZIP=awscli-exe-linux-x86_64.zip

wget -O ~/Downloads/${AWS_CLI_ZIP} https://awscli.amazonaws.com/${AWS_CLI_ZIP}

unzip ~/Downloads/${AWS_CLI_ZIP} -d ~/Downloads

sudo ~/Downloads/aws/install
