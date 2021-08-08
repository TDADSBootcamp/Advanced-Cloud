import random
import string
import os
import sys
import json

from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_iam as iam
from aws_cdk import cloudformation_include as cfn_inc
from aws_cdk import aws_budgets as budgets
from aws_cdk import aws_sagemaker as sm

import infrastructure.emr_cluster as emr_cluster


def random_string(length: int) -> str:
  '''
    >>> import re
    >>> assert re.match(r'^[a-z]+$', random_string(100))
    '''
  return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


class InfrastructureStack(cdk.Stack):

  def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    billing_alert_emails = os.environ['BILLING_ALERT_EMAILS'].split(',')

    example_bucket = s3.Bucket(self, 'example-bucket', versioned=True)
    # so that stack does not fail if there are objects in the bucket
    example_bucket.apply_removal_policy(cdk.RemovalPolicy.RETAIN)

    student_group = iam.Group(
        self,
        'students',
        group_name='students',
        managed_policies=[
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonAthenaFullAccess'),
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AWSGlueConsoleFullAccess'),
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonS3FullAccess')
        ])

    student_group.add_to_policy(
        iam.PolicyStatement(actions=['s3:*'],
                            resources=[example_bucket.bucket_arn]))

    with open(os.path.join(sys.path[0],
                           'user_credentials_policy.json')) as policy_json:
      student_group.attach_inline_policy(
          iam.Policy(self,
                     'manage-creds',
                     document=iam.PolicyDocument.from_json(
                         json.load(policy_json))))

    covid_data_lake_template = cfn_inc.CfnInclude(
        self,
        'covid-data-lake-glue',
        template_file='CovidLakeStack.template.json',
        preserve_logical_ids=False)

    budget = budgets.CfnBudget(
        self,
        'budget',
        budget=budgets.CfnBudget.BudgetDataProperty(
            budget_type='COST',
            time_unit='MONTHLY',
            budget_limit=budgets.CfnBudget.SpendProperty(amount=10,
                                                         unit='USD')),
        notifications_with_subscribers=[
            budgets.CfnBudget.NotificationWithSubscribersProperty(
                notification=budgets.CfnBudget.NotificationProperty(
                    comparison_operator='GREATER_THAN',
                    notification_type='ACTUAL',
                    threshold=80),
                subscribers=[
                    budgets.CfnBudget.SubscriberProperty(
                        subscription_type='EMAIL', address=targetAddress)
                    for targetAddress in billing_alert_emails
                ])
        ])

    notebook_role = iam.Role(self,
                             'notbooks_access_role',
                             assumed_by=iam.ServicePrincipal('sagemaker'),
                             managed_policies=[
                                 iam.ManagedPolicy.from_aws_managed_policy_name(
                                     'AmazonSageMakerFullAccess')
                             ])

    notebook_policy = iam.Policy(self,
                                 'notebook_access_policy',
                                 policy_name='notebook_access_policy',
                                 statements=[
                                     iam.PolicyStatement(
                                         actions=['s3:*'],
                                         resources=[example_bucket.bucket_arn])
                                 ]).attach_to_role(notebook_role)

    # instance = sm.CfnNotebookInstance(self,
    #                                   'notebook',
    #                                   instance_type='ml.t2.medium',
    #                                   volume_size_in_gb=5,
    #                                   notebook_instance_name='notebook',
    #                                   role_arn=notebook_role.role_arn)
