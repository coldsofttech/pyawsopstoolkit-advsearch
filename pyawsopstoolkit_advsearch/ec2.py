from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

from pyawsopstoolkit_advsearch import OR, AND
from pyawsopstoolkit_advsearch.__globals__ import MAX_WORKERS
from pyawsopstoolkit_advsearch.__validations__ import _validate_type
from pyawsopstoolkit_advsearch.exceptions import AdvanceSearchError, SearchAttributeError
from pyawsopstoolkit_advsearch.search import _match_tag_condition, _match_number_condition, \
    _match_number_range_condition, _match_condition, _match_bool_condition

BOTO3_CLIENT = 'ec2'


def _get_security_group_usage(session, region, security_group_id) -> bool:
    """
    Utilizing boto3 IAM, this method verifies if the specified security_group_id is associated with any ENI (Elastic
    Network Interface). Reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_network_interfaces.html
    """
    from botocore.config import Config
    from botocore.exceptions import ClientError

    usage = False

    try:
        if session.cert_path:
            ec2_client = session.get_session().client(BOTO3_CLIENT, config=Config(region), verify=session.cert_path)
        else:
            ec2_client = session.get_session().client(BOTO3_CLIENT, config=Config(region))

        ec2_response = ec2_client.describe_network_interfaces(
            Filters=[{
                "Name": "group-id",
                "Values": [security_group_id]
            }]
        )
        if ec2_response:
            usage = True if len(ec2_response.get('NetworkInterfaces', [])) > 0 else False
    except ClientError as e:
        raise e

    return usage


def _list_security_groups(session, region) -> list:
    """
    Utilizing boto3 IAM, this method retrieves a list of all security groups leveraging the provided ISession object.
    Reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSecurityGroups.html

    :param session: The Session object which provide access to AWS services.
    :type session: pyawsopstoolkit.session.Session
    :param region: The region to search security groups for.
    :type region: str
    :return: A list of EC2 security groups.
    :rtype: list
    """
    from botocore.config import Config
    from botocore.exceptions import ClientError

    security_groups_to_process = []

    try:
        if session.cert_path:
            ec2_client = session.get_session().client(BOTO3_CLIENT, config=Config(region), verify=session.cert_path)
        else:
            ec2_client = session.get_session().client(BOTO3_CLIENT, config=Config(region))
        ec2_paginator = ec2_client.get_paginator('describe_security_groups')

        for page in ec2_paginator.paginate():
            security_groups_to_process.extend(page.get('SecurityGroups', []))
    except ClientError as e:
        raise e

    return security_groups_to_process


@dataclass
class SecurityGroup:
    """
    A class representing advance search features related with EC2 security groups.
    """
    from pyawsopstoolkit.account import Account
    from pyawsopstoolkit.session import Session

    session: Session

    def __post_init__(self):
        for field_name, field_value in self.__dataclass_fields__.items():
            self.__validate__(field_name)

    def __validate__(self, field_name):
        from pyawsopstoolkit.session import Session

        field_value = getattr(self, field_name)
        if field_name in ['session']:
            _validate_type(field_value, Session, f'{field_name} should be of Session type.')

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self.__dataclass_fields__:
            self.__validate__(key)

    @staticmethod
    def _convert_to_ec2_security_group(account: Account, region: str, sg: dict):
        """
        This function transforms the dictionary response from boto3 EC2 into a format compatible with the AWS Ops
        Toolkit, adhering to the pyawsopstoolkit_models structure. Additionally, it incorporates account-related
        summary information into the EC2 security group details.

        :param account: An Account object containing AWS account information.
        :type account: pyawsopstoolkit.account.Account
        :param region: The region associated with the EC2 security group.
        :type region: str
        :param sg: The boto3 EC2 service response for the security group.
        :type sg: dict
        :return: An AWS Ops Toolkit compatible object containing all EC2 security group details.
        :rtype: pyawsopstoolkit_models.ec2.security_group.SecurityGroup
        """
        from pyawsopstoolkit_models.ec2.security_group import IPPermission, IPRange, IPv6Range, PrefixList, \
            SecurityGroup, UserIDGroupPair

        def _create_ip_permission(perm):
            ip_permission = IPPermission(
                from_port=perm.get('FromPort', 0),
                to_port=perm.get('ToPort', 0),
                ip_protocol=perm.get('IpProtocol', '')
            )

            ip_permission.ip_ranges = [
                IPRange(cidr_ip=ip.get('CidrIp', ''), description=ip.get('Description', ''))
                for ip in perm.get('IpRanges', [])
            ]

            ip_permission.ipv6_ranges = [
                IPv6Range(cidr_ipv6=ip.get('CidrIpv6', ''), description=ip.get('Description', ''))
                for ip in perm.get('Ipv6Ranges', [])
            ]

            ip_permission.prefix_lists = [
                PrefixList(id=prefix.get('PrefixListId', ''), description=prefix.get('Description', ''))
                for prefix in perm.get('PrefixListIds', [])
            ]

            ip_permission.user_id_group_pairs = [
                UserIDGroupPair(
                    id=pair.get('GroupId', ''),
                    name=pair.get('GroupName', ''),
                    status=pair.get('PeeringStatus', ''),
                    user_id=pair.get('UserId', ''),
                    vpc_id=pair.get('VpcId', ''),
                    description=pair.get('Description', ''),
                    vpc_peering_connection_id=pair.get('VpcPeeringConnectionId', '')
                )
                for pair in perm.get('UserIdGroupPairs', [])
            ]

            return ip_permission

        ec2_security_group = SecurityGroup(
            account=account,
            region=region,
            id=sg.get('GroupId', ''),
            name=sg.get('GroupName', ''),
            owner_id=sg.get('OwnerId', ''),
            vpc_id=sg.get('VpcId', '')
        )

        ec2_security_group.ip_permissions = [
            _create_ip_permission(perm) for perm in sg.get('IpPermissions', [])
        ]

        ec2_security_group.ip_permissions_egress = [
            _create_ip_permission(perm) for perm in sg.get('IpPermissionsEgress', [])
        ]

        ec2_security_group.tags = sg.get('Tags', [])

        return ec2_security_group

    def search_security_groups(
            self,
            condition: str = OR,
            region: str | list = 'eu-west-1',
            include_usage: bool = False,
            **kwargs
    ) -> list:
        """
        Returns a list of EC2 security groups using advanced search feature supported by the specified arguments. For
        details on supported kwargs, please refer to the readme document.

        :param condition: The condition to be applied: 'OR' or 'AND'.
        :type condition: str
        :param region: The region or list of regions to search for EC2 security groups. Defaults to eu-west-1.
        :type region: str | list
        :param include_usage: Flag to indicate if verify if EC2 security group is associated with any ENI (Elastic
        Network Interface).
        :type include_usage: bool
        :param kwargs: Key-based arguments defining search criteria.
        :return: A list of EC2 security groups.
        :rtype: list
        """
        from pyawsopstoolkit_validators.region_validator import region as region_val

        _validate_type(condition, str, 'condition should be a string and should be either "OR" or "AND".')
        if isinstance(region, str):
            region_val(region, True)
        elif isinstance(region, list):
            all(region_val(r, True) for r in region)
        else:
            raise ValueError('region should be a string or list of strings.')

        def _process_security_group(sg_detail, _region):
            sg = self._convert_to_ec2_security_group(self.session.get_account(), _region, sg_detail)
            if include_usage:
                sg.in_use = _get_security_group_usage(self.session, _region, sg_detail.get('GroupId', ''))

            return sg

        def _match_security_group(sg_detail, _region):
            if sg_detail:
                matched = False if condition == OR else True
                for key, value in kwargs.items():
                    if value is not None:
                        sg_field = ''
                        if key.lower() == 'id':
                            sg_field = sg_detail.get('GroupId', '')
                        elif key.lower() == 'name':
                            sg_field = sg_detail.get('GroupName', '')
                        elif key.lower() == 'owner_id':
                            sg_field = sg_detail.get('OwnerId', '')
                        elif key.lower() == 'vpc_id':
                            sg_field = sg_detail.get('VpcId', '')
                        elif key.lower() == 'description':
                            sg_field = sg_detail.get('Description', '')
                        elif key.lower() == 'tag_key':
                            tags = {tag['Key']: tag['Value'] for tag in sg_detail.get('Tags', [])}
                            matched = _match_tag_condition(value, tags, condition, matched, key_only=True)
                        elif key.lower() == 'tag':
                            tags = {tag['Key']: tag['Value'] for tag in sg_detail.get('Tags', [])}
                            matched = _match_tag_condition(value, tags, condition, matched, key_only=False)
                        elif key.lower() == 'in_from_port':
                            ip_permissions = sg_detail.get('IpPermissions', [])
                            sg_field = [ip_prem.get('FromPort', 0) for ip_prem in ip_permissions]
                            matched = _match_number_condition(value, sg_field, condition, matched)
                        elif key.lower() == 'out_from_port':
                            ip_permissions = sg_detail.get('IpPermissionsEgress', [])
                            sg_field = [ip_prem.get('FromPort', 0) for ip_prem in ip_permissions]
                            matched = _match_number_condition(value, sg_field, condition, matched)
                        elif key.lower() == 'in_to_port':
                            ip_permissions = sg_detail.get('IpPermissions', [])
                            sg_field = [ip_prem.get('ToPort', 0) for ip_prem in ip_permissions]
                            matched = _match_number_condition(value, sg_field, condition, matched)
                        elif key.lower() == 'out_to_port':
                            ip_permissions = sg_detail.get('IpPermissionsEgress', [])
                            sg_field = [ip_prem.get('ToPort', 0) for ip_prem in ip_permissions]
                            matched = _match_number_condition(value, sg_field, condition, matched)
                        elif key.lower() == 'in_port_range':
                            ip_permissions = sg_detail.get('IpPermissions', [])
                            sg_field = [
                                (ip_prem.get('FromPort', 0), ip_prem.get('ToPort', 0)) for ip_prem in ip_permissions
                            ]
                            matched = _match_number_range_condition(value, sg_field, condition, matched)
                        elif key.lower() == 'out_port_range':
                            ip_permissions = sg_detail.get('IpPermissionsEgress', [])
                            sg_field = [
                                (ip_prem.get('FromPort', 0), ip_prem.get('ToPort', 0)) for ip_prem in ip_permissions
                            ]
                            matched = _match_number_range_condition(value, sg_field, condition, matched)
                        elif key.lower() == 'in_ip_protocol':
                            ip_permissions = sg_detail.get('IpPermissions', [])
                            sg_field = [
                                ip_prem.get('IpProtocol', '').replace('-1', 'all') for ip_prem in ip_permissions
                            ]
                        elif key.lower() == 'out_ip_protocol':
                            ip_permissions = sg_detail.get('IpPermissionsEgress', [])
                            sg_field = [
                                ip_prem.get('IpProtocol', '').replace('-1', value) for ip_prem in ip_permissions
                            ]
                        elif key.lower() == 'in_use':
                            if include_usage:
                                sg_field = _get_security_group_usage(self.session, region, sg_detail.get('GroupId', ''))
                                matched = _match_bool_condition(value, sg_field, condition, matched)

                        if key.lower() not in [
                            'tag_key', 'tag', 'in_from_port', 'out_from_port', 'in_to_port', 'out_to_port',
                            'in_port_range', 'out_port_range', 'in_use'
                        ]:
                            matched = _match_condition(value, sg_field, condition, matched)

                        if (condition == OR and matched) or (condition == AND and not matched):
                            break

                if matched:
                    return _process_security_group(sg_detail, _region)

        security_groups_to_return = []
        regions_to_process = [region] if isinstance(region, str) else region

        from botocore.exceptions import ClientError
        try:
            include_usage_keys = {
                'in_use'
            }

            if not include_usage and any(k in include_usage_keys for k in kwargs):
                raise SearchAttributeError(
                    f'include_usage is required for below keys: {", ".join(sorted(include_usage_keys))}'
                )

            for _region in regions_to_process:
                security_groups_to_process = _list_security_groups(self.session, _region)

                if len(kwargs) == 0:
                    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                        future_to_sg = {
                            executor.submit(_process_security_group, sg, _region): sg
                            for sg in security_groups_to_process
                        }
                        for future in as_completed(future_to_sg):
                            sg_result = future.result()
                            if sg_result is not None:
                                security_groups_to_return.append(sg_result)
                else:
                    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                        future_to_sg = {
                            executor.submit(_match_security_group, sg, _region): sg
                            for sg in security_groups_to_process
                        }
                        for future in as_completed(future_to_sg):
                            sg_result = future.result()
                            if sg_result is not None:
                                security_groups_to_return.append(sg_result)
        except ClientError as e:
            raise AdvanceSearchError('search_security_groups', e)

        return security_groups_to_return
