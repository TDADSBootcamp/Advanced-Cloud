#!/bin/bash

set -euo pipefail

echo "Pre-reqs: cdk, member AWS account, admin-level role in target account with org account able to assume, ~/.aws/config with target role configured"

export ACCOUNT_ID=$1
export AWS_PROFILE=$2
export BILLING_ALERT_EMAILS=$3
export REGION=${4:-eu-west-2}

aws iam update-account-password-policy \
  --minimum-password-length 20 \
  --no-require-symbols \
  --no-require-numbers \
  --no-require-uppercase-characters \
  --allow-users-to-change-password \
  --password-reuse-prevention 10

npx cdk bootstrap aws://${ACCOUNT_ID}/${REGION}

npx cdk deploy
