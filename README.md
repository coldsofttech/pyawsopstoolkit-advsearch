# pyawsopstoolkit_advsearch

The **pyawsopstoolkit_advsearch** module delivers an exhaustive array of advanced search functionalities, tailor-made
for seamless integration with AWS (Amazon Web Services). Meticulously engineered, these advanced searches are finely
tuned to meet the distinctive demands inherent to the expansive AWS ecosystem, encompassing a diverse spectrum of
aspects.

## Getting Started

Ready to supercharge your AWS operations? Let's get started with **pyawsopstoolkit_advsearch!**

### Installation

Install **pyawsopstoolkit_advsearch** via pip:

```bash
pip install pyawsopstoolkit_advsearch
```

## Documentation

- [Constants](#constants)
- [ec2](#ec2)
- [iam](#iam)

### Constants

This package supports various conditions for advanced searches, outlined below as global constants:

- `OR`: Represents the **or** condition.
- `AND`: Represents the **and** condition.
- `LESS_THAN`: Represents the less than **<** value.
- `LESS_THAN_OR_EQUAL_TO`: Represents the less than or equal to **<=** value.
- `GREATER_THAN`: Represents the greater than **>** value.
- `GREATER_THAN_OR_EQUAL_TO`: Represents the greater than or equal to **>=** value.
- `EQUAL_TO`: Represents the equal to **=** value.
- `NOT_EQUAL_TO`: Represents the not equal to **!=** value.
- `BETWEEN`: Represents the between range **< x <** value. These constants facilitate the formulation of complex
  queries, enabling precise and efficient data retrieval within the AWS environment.

### ec2

This **pyawsopstoolkit_advsearch.ec2** subpackage offers sophisticated search capabilities specifically designed for
AWS (Amazon Web Services) Elastic Compute Cloud (EC2).

#### SecurityGroup

The **SecurityGroup** class provides advanced search features related to EC2 security groups.

##### Constructors

- `SecurityGroup(session: Session) -> None`: Initializes a new **SecurityGroup** object.

##### Methods

- `search_security_groups(condition: str = OR, region: str | list = 'eu-west-1', include_usage: bool = False, **kwargs) -> list`:
  Returns a list of EC2 security groups using advanced search features supported by the specified arguments. For details
  on supported keyword arguments, please refer to the section below.

##### Properties

- `session`: An `pyawsopstoolkit.session.Session` object providing access to AWS services.

##### `search_security_groups` Supported Keyword Arguments

The **search_security_groups** method allows you to search for EC2 security groups using various keyword arguments.
Below are the supported keyword arguments:

- `description`: Specifies the description of the EC2 security group. Example: `description='test'`.
- `id`: Specifies the unique identifier of the EC2 security group. Example: `id='sg-12345678'`.
- `in_use`: Specifies the flag to indicate if the EC2 security group has any associated ENIs. Example: `in_use=True`.
- `in_from_port`: Specifies the inbound EC2 security group rule entry "from" port. Example: `in_from_port=80`.
- `in_ip_protocol`: Specifies the inbound EC2 security group rule entry protocol. Example: `in_ip_protocol='tcp'`.
- `in_port_range`: Specifies the inbound EC2 security group rule entry port if it exists within range "from" and "to".
  Example: `in_port_range=80`.
- `in_to_port`: Specifies the inbound EC2 security group rule entry "to" port. Example: `in_to_port=443`.
- `name`: Specifies the name of the EC2 security group. Example: `name='web-servers-sg'`.
- `out_from_port`: Specifies the outbound EC2 security group rule entry "from" port. Example: `out_from_port=80`.
- `out_ip_protocol`: Specifies the outbound EC2 security group rule entry protocol. Example: `out_ip_protocol='udp'`.
- `out_port_range`: Specifies the outbound EC2 security group rule entry port if it exists within range "from" and "to".
  Example: `out_port_range=443`.
- `out_to_port`: Specifies the outbound EC2 security group rule entry "to" port. Example: `out_to_port=443`.
- `owner_id`: Specifies the owner ID of the EC2 security group. Example: `owner_id='123456789012'`.
- `tag_key`: Specifies the tag key associated with the EC2 security group. Example: `tag_key='test_key'`.
- `tag`: Specifies the tag key and value combination associated with the EC2 security group (dictionary format).
  Example: `tag={'key': 'test_key', 'value': 'test_value'}`.
- `vpc_id`: Specifies the VPC ID of the EC2 security group. Example: `vpc_id='vpc-abcdefgh'`.

All the above arguments support string types and accept regular expression patterns. Additionally,
the `in_from_port`, `out_from_port`, `in_to_port`, `out_to_port`, `in_port_range`, and `out_port_range` arguments
support integer types.

###### Usage

```python
from pyawsopstoolkit.session import Session
from pyawsopstoolkit_advsearch.ec2 import SecurityGroup
from pyawsopstoolkit_advsearch import OR

# Create a session using the 'default' profile
session = Session(profile_name='default')

# Initialize the EC2 security group object with the session
sg_object = SecurityGroup(session=session)

# Example searches:

# 1. Search for all EC2 security groups
print(sg_object.search_security_groups())

# 2. Search for EC2 security groups with the name matching 'test_sg'
print(sg_object.search_security_groups(condition=OR, region='us-east-2', name=r'test_sg'))

# 3. Search for EC2 security groups with the name matching 'test_sg' or description matching 'test'
print(sg_object.search_security_groups(condition=OR, region='us-east-2', name=r'test_sg', description=r'test'))

# 4. Search for EC2 security groups that contain the tag key 'test_key'
print(sg_object.search_security_groups(tag_key='test_key'))

# 5. Search for EC2 security groups that contain a tag with key 'test_key' and value 'test_value'
print(sg_object.search_security_groups(tag={'key': 'test_key', 'value': 'test_value'}))

# 6. Search for EC2 security groups that contain port 80 as an inbound rule entry
print(sg_object.search_security_groups(in_from_port=80))

# 7. Search for EC2 security groups that contain 'all' traffic within inbound rule entry protocols
print(sg_object.search_security_groups(in_ip_protocol='all'))

# 8. Search for EC2 security groups that are in use and associated with ENIs
print(sg_object.search_security_groups(include_usage=True, in_use=True))
```

### iam

This **pyawsopstookit_advsearch.iam** subpackage offers sophisticated search capabilities specifically designed for
AWS (Amazon Web Services) Identity and Access Management (IAM).

#### Role

A class representing advanced search features related to IAM roles.

##### Constructors

- `Role(session: Session) -> None`: Initializes a new **Role** object.

##### Methods

- `search_roles(condition: str = OR, include_details: bool = False, **kwargs) -> list`: Returns a list of IAM roles
  using advanced search features supported by the specified arguments. For details on supported kwargs, please refer to
  the section below.

##### Properties

- `session`: An `pyawsopstoolkit.session.Session` object providing access to AWS services.

##### `search_roles` Supported Keyword Arguments

The **search_roles** function allows you to search for IAM roles using various keyword arguments. Below are the
supported keyword arguments:

- `arn`: Specifies the ARN of the IAM role. Example: `arn='arn:aws:iam::111122223333:role/role-name'`.
- `created_date`: Specifies the created date of the IAM role (datetime format).
  Example: `created_date={GREATER_THAN: datetime(2024, 10, 15)}`.
- `description`: Specifies the description of the IAM role. Example: `description='test'`.
- `id`: Specifies the ID of the IAM role. Example: `id='AIDACKCEVSQ6C2EXAMPLE'`.
- `last_used_date`: Specifies the last used date of the IAM role (datetime format).
  Example: `last_used_date={BETWEEN: [datetime(2023, 10, 15), datetime(2024, 10, 15)]}`.
- `last_used_region`: Specifies the region where the IAM role was last used. Example: `last_used_region='eu-west-1'`.
- `max_session_duration`: Specifies the maximum session duration of the IAM role (in seconds, integer type).
  Example: `max_session_duration={LESS_THAN: 3600}`.
- `name`: Specifies the name of the IAM role. Example: `name='test_role'`.
- `path`: Specifies the path of the IAM role. Example: `path='/service-role/'`.
- `permissions_boundary_arn`: Specifies the ARN of the permissions boundary for the IAM role.
  Example: `permissions_boundary_arn='arn:aws:iam::111122223333:policy/policy-name'`.
- `permissions_boundary_type`: Specifies the type of permissions boundary for the IAM role.
  Example: `permissions_boundary_type='Policy'`.
- `tag_key`: Specifies the tag key associated with the IAM role. Example: `tag_key='test_key'`.
- `tag`: Specifies the tag key and value combination associated with the IAM role (dictionary format).
  Example: `tag={'key': 'test_key', 'value': 'test_value'}`.

All the above arguments support string types and accept regular expression patterns. Additionally,
the `max_session_duration`, `created_date`, and `last_used_date` arguments support conditions such as less than, greater
than, and between. For more details, please refer to the constants above.

###### Usage

```python
from datetime import datetime

from pyawsopstoolkit.session import Session
from pyawsopstoolkit_advsearch.iam import Role
from pyawsopstoolkit_advsearch import OR, AND, LESS_THAN, BETWEEN

# Create a session using the 'default' profile
session = Session(profile_name='default')

# Initialize the IAM Role object with the session
role_object = Role(session=session)

# Example searches:
# 1. Search for all IAM roles
print(role_object.search_roles())

# 2. Search for IAM roles with the name matching 'test_role'
print(role_object.search_roles(condition=OR, name=r'test_role'))

# 3. Search for IAM roles with the name matching 'test_role' or description matching 'test'
print(role_object.search_roles(condition=OR, name=r'test_role', description=r'test'))

# 4. Search for IAM roles with both path matching '/service-role/' and name matching 'test'
print(role_object.search_roles(condition=AND, path='/service-role/', name='test'))

# 5. Search for IAM roles with a maximum session duration less than 4 hours (14400 seconds)
print(role_object.search_roles(max_session_duration={LESS_THAN: 14400}))

# 6. Search for IAM roles last used between October 15, 2023, and October 15, 2024
print(role_object.search_roles(last_used_date={BETWEEN: [datetime(2023, 10, 15), datetime(2024, 10, 15)]}))

# 7. Search for IAM roles that contain the tag key 'test_key'
print(role_object.search_roles(tag_key='test_key'))

# 8. Search for IAM roles that contain a tag with key 'test_key' and value 'test_value'
print(role_object.search_roles(tag={'key': 'test_key', 'value': 'test_value'}))
```

#### User

A class representing advance search features related with IAM users.

##### Constructors

- `User(session: Session) -> None`: Initializes a new **User** object.

##### Methods

- `search_users(condition: str = OR, include_details: bool = False, **kwargs) -> list`: Returns a list of IAM users
  using advanced search features supported by the specified arguments. For details on supported kwargs, please refer to
  the section below.

##### Properties

- `session`: An `pyawsopstoolkit.session.Session` object providing access to AWS services.

##### `search_users` Supported Keyword Arguments

The `search_users` function allows you to search for IAM users using various keyword arguments. Below are the supported
keyword arguments:

- `access_key_id`: Specifies the ID of the IAM user access key. Example: `access_key_id='ABCD'`.
- `access_key_region`: Specifies the last used region of the IAM user access key.
  Example: `access_key_region='eu-west-1'`.
- `access_key_service`: Specifies the last used service of the IAM user access key.
  Example: `access_key_service='ec2.amazonaws.com'`.
- `access_key_status`: Specifies the status of the IAM user access key. Example: `access_key_status='Active'`.
- `arn`: Specifies the ARN of the IAM user. Example: `arn='arn:aws:iam::111122223333:user/test_user'`.
- `created_date`: Specifies the created date of the IAM user (datetime format).
  Example: `created_date={GREATER_THAN: datetime(2024, 10, 15)}`.
- `id`: Specifies the ID of the IAM user. Example: `id='AIDACKCEVSQ6C2EXAMPLE'`.
- `login_profile_created_date`: Specifies the login profile created date of the IAM user (datetime format).
  Example: `login_profile_created_date={GREATER_THAN: datetime(2024, 10, 15)}`.
- `login_profile_password_reset_required`: Specifies the flag of the login profile to check if a password reset is
  required for the IAM user (boolean format). Example: `login_profile_password_reset_required=False`.
- `name`: Specifies the name of the IAM user. Example: `name='test_user'`.
- `password_last_used_date`: Specifies the password last used date of the IAM user (datetime format).
  Example: `password_last_used_date={BETWEEN: [datetime(2023, 10, 15), datetime(2024, 10, 15)]}`.
- `path`: Specifies the path of the IAM user. Example: `path='/'`.
- `permissions_boundary_arn`: Specifies the ARN of the permissions boundary for the IAM user.
  Example: `permissions_boundary_arn='arn:aws:iam::111122223333:policy/policy-name'`.
- `permissions_boundary_type`: Specifies the type of permissions boundary for the IAM user.
  Example: `permissions_boundary_type='Policy'`.
- `tag_key`: Specifies the tag key associated with the IAM user. Example: `tag_key='test_key'`.
- `tag`: Specifies the tag key and value combination associated with the IAM user (dictionary format).
  Example: `tag={'Key': 'test_key', 'Value': 'test_value'}`.

All the above arguments support string types and accept regular expression patterns. Additionally, the `created_date`
and `password_last_used_date` arguments support conditions such as less than, greater than, and between. For more
details, please refer to the constants above.

###### Usage

```python
from datetime import datetime

from pyawsopstoolkit.session import Session
from pyawsopstoolkit_advsearch.iam import User
from pyawsopstoolkit_advsearch import OR, AND, BETWEEN

# Create a session using the 'default' profile
session = Session(profile_name='default')

# Initialize the IAM User object with the session
user_object = User(session=session)

# Example searches:
# 1. Search for all IAM users
print(user_object.search_users())

# 2. Search for IAM users with the name matching 'test_user'
print(user_object.search_users(condition=OR, name=r'test_user'))

# 3. Search for IAM users with both path matching '/' and name matching 'test'
print(user_object.search_users(condition=AND, path='/', name='test'))

# 4. Search for IAM users password last used between October 15, 2023, and October 15, 2024
print(user_object.search_users(password_last_used_date={BETWEEN: [datetime(2023, 10, 15), datetime(2024, 10, 15)]}))

# 5. Search for IAM roles that contain the tag key 'test_key'
print(user_object.search_users(tag_key='test_key'))

# 6. Search for IAM roles that contain a tag with key 'test_key' and value 'test_value'
print(user_object.search_users(tag={'key': 'test_key', 'value': 'test_value'}))
```

# License

Please refer to the [MIT License](LICENSE) within the project for more information.

# Contributing

We welcome contributions from the community! Whether you have ideas for new features, bug fixes, or enhancements, feel
free to open an issue or submit a pull request on [GitHub](https://github.com/coldsofttech/pyawsopstoolkit-advsearch).