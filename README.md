Supporting materials for Data Science Bootcamp - Cloud 1 & 2

# Instructor

## Setup Infra (Before the session #1)

The infrastructure for the session is IaC, defined with [CDK](https://docs.aws.amazon.com/cdk/latest/guide/home.html).

Setup instructions are found in [infrastructure](infrastructure).

## Setup (During the session)

Once the stack is deployed, users can be created with [./setup_user.sh username profile](setup_user.sh).

For each student, create a user with an appropriate username.
The new user will have a randomly generated password and require a reset at first login.

On Linux, the password will be copied into your clipboard (you'll need xclip installed).
You'll need to modify the script if you're not running Linux.
Paste the password into a DM with the student.

MFA will be required for the student to generate access keys for the AWS CLI.

