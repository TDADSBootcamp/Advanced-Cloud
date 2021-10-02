import typing
import argparse

import boto3
from botocore.exceptions import ClientError

class Args(typing.NamedTuple):
  profile: str


def parse_args() -> Args:
  parser = argparse.ArgumentParser(description='User admin functions')
  parser.add_argument('--profile', default='default', help='AWS profile to use for these operations')

  parsed = parser.parse_args()
  return Args(profile=parsed.profile)

def get_student_group(session, student_group_name: str = 'students'):
  iam = session.resource('iam')
  students = iam.Group(student_group_name)

  try:
    return students.load()
  except ClientError as ce:
    if ce.response['Error']['Code'] == 'NoSuchEntity':
      return None
    else:
      raise ce

def delete_user(user):
  print(f'Deleting user "{user.user_name}"')

  print('Deleting access keys...')
  for key in user.access_keys.all():
    key.delete()

  print('Dissociating from groups...')
  for group in user.groups.all():
    user.remove_group(GroupName=group.name)

  print('Dissociating MFA devices...')
  for mfa_device in user.mfa_devices.all():
    mfa_device.disassociate()

  print('Deleting login profile...')
  if user.LoginProfile():
    user.LoginProfile().delete()

  print('Deleting user account...')
  user.delete()

  print('Done')


def clear_student_group(group):
  print(f'Clearing policies in group {group.name}')
  for policy in group.policies.all():
    policy.delete()

  for policy in group.attached_policies.all():
    policy.detach_group(GroupName=group.name)


def delete_buckets(session):
  for bucket_name in (bucket['Name'] for bucket in session.client('s3').list_buckets()['Buckets'] if 'cdktoolkit' not in bucket['Name']):
    print(f'Clearing and deleting bucket "{bucket_name}"')
    bucket = session.resource('s3').Bucket(bucket_name)
    if bucket.Versioning().status == 'Enabled':
      bucket.object_versions.all().delete()
    bucket.objects.all().delete()
    bucket.delete()


def main(args: Args):
  session = boto3.session.Session(profile_name=args.profile)

  delete_buckets(session)

  student_group = get_student_group(session)

  if student_group:
    student_users = list(student_group.users.all())

    for user in student_users:
      delete_user(user)

    clear_student_group(student_group)

if __name__ == '__main__':
  args = parse_args()
  main(args)
