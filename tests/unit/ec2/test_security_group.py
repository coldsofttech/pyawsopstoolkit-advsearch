import unittest
from unittest import mock
from unittest.mock import patch, MagicMock

from pyawsopstoolkit_advsearch import OR
from pyawsopstoolkit_advsearch.ec2 import SecurityGroup


class TestSecurityGroup(unittest.TestCase):
    def setUp(self) -> None:
        from pyawsopstoolkit.session import Session

        self.profile_name = 'temp'
        self.session = Session(profile_name=self.profile_name)
        self.security_group = SecurityGroup(session=self.session)

    def test_initialization(self):
        self.assertEqual(self.security_group.session, self.session)

    def test_setters(self):
        from pyawsopstoolkit.session import Session

        new_session = Session(profile_name='sample')
        self.security_group.session = new_session
        self.assertEqual(self.security_group.session, new_session)

    def test_invalid_types(self):
        invalid_session = 123

        with self.assertRaises(TypeError):
            SecurityGroup(session=invalid_session)
        with self.assertRaises(TypeError):
            self.security_group.session = invalid_session

    @patch('boto3.Session')
    def test_search_security_groups_empty_kwargs(self, mock_session):
        session_instance = mock_session.return_value
        session_instance.client.return_value.list_buckets.return_value = {}

        self.assertEqual(len(self.security_group.search_security_groups()), 0)

    @patch('boto3.Session')
    def test_search_security_groups_all_none(self, mock_session):
        session_instance = mock_session.return_value
        session_instance.client.return_value.list_buckets.return_value = {}

        self.assertEqual(
            len(self.security_group.search_security_groups(condition=OR, name=None, id=None)), 0
        )

    @patch('boto3.Session')
    @patch('pyawsopstoolkit.session.Session.get_session')
    @patch('pyawsopstoolkit_advsearch.ec2._list_security_groups', return_value=[{
        'Description': 'Web server security group',
        'GroupName': 'web-servers',
        'OwnerId': '123456789012',
        'GroupId': 'sg-12345678',
        'VpcId': 'vpc-12345678'
    }])
    @patch('pyawsopstoolkit_advsearch.__validations__._validate_type', return_value=None)
    def test_search_security_groups_basic(
            self, mock_validation, mock_list_security_groups, mock_get_session, mock_session
    ):
        from pyawsopstoolkit.account import Account
        from pyawsopstoolkit_models.ec2.security_group import SecurityGroup

        mock_client = MagicMock()
        mock_caller_identity = MagicMock()

        mock_caller_identity.get.return_value = '123456789012'
        mock_client.get_caller_identity.return_value = mock_caller_identity
        mock_get_session.return_value.client.return_value = mock_client

        session_instance = mock_session.return_value
        session_instance.client.return_value.list_buckets.return_value = {}

        sgs_data = mock_list_security_groups.return_value
        security_groups = [SecurityGroup(
            account=Account('123456789012'),
            region='eu-west-1',
            id=sg_data['GroupId'],
            name=sg_data['GroupName'],
            owner_id=sg_data['OwnerId'],
            vpc_id=sg_data['VpcId']
        ) for sg_data in sgs_data]
        self.security_group.search_security_groups = mock.Mock(return_value=security_groups)

        result = self.security_group.search_security_groups(condition=OR, name='web-servers', id='sg-12345678')

        self.assertEqual(result[0].name, 'web-servers')
        self.assertIsNone(result[0].ip_permissions)
        self.assertIsNone(result[0].ip_permissions_egress)
        self.assertIsNone(result[0].tags)

    @patch('boto3.Session')
    @patch('pyawsopstoolkit.session.Session.get_session')
    @patch('pyawsopstoolkit_advsearch.ec2._list_security_groups', return_value=[{
        'Description': 'Main security group for the application',
        'GroupName': 'AppSecurityGroup',
        'IpPermissions': [
            {
                'FromPort': 80,
                'IpProtocol': 'tcp',
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0',
                        'Description': 'Allow all traffic from IPv4'
                    }
                ],
                'Ipv6Ranges': [
                    {
                        'CidrIpv6': '::/0',
                        'Description': 'Allow all traffic from IPv6'
                    }
                ],
                'PrefixListIds': [
                    {
                        'Description': 'Allow traffic from prefix list',
                        'PrefixListId': 'pl-12345abcde'
                    }
                ],
                'ToPort': 80,
                'UserIdGroupPairs': [
                    {
                        'Description': 'Allow traffic from admin security group',
                        'GroupId': 'sg-67890fghij',
                        'GroupName': 'AdminSecurityGroup',
                        'PeeringStatus': 'active',
                        'UserId': '123456789012',
                        'VpcId': 'vpc-abcde12345',
                        'VpcPeeringConnectionId': 'pcx-abc123de'
                    }
                ]
            }
        ],
        'OwnerId': '123456789012',
        'GroupId': 'sg-abcdef123456',
        'VpcId': 'vpc-12345abcde'
    }])
    @patch('pyawsopstoolkit_advsearch.__validations__._validate_type', return_value=None)
    def test_search_security_groups_with_ip_permissions(
            self, mock_validation, mock_list_security_groups, mock_get_session, mock_session
    ):
        from pyawsopstoolkit.account import Account
        from pyawsopstoolkit_models.ec2.security_group import SecurityGroup, IPPermission, IPRange, IPv6Range, \
            PrefixList, UserIDGroupPair

        mock_client = MagicMock()
        mock_caller_identity = MagicMock()

        mock_caller_identity.get.return_value = '123456789012'
        mock_client.get_caller_identity.return_value = mock_caller_identity
        mock_get_session.return_value.client.return_value = mock_client

        session_instance = mock_session.return_value
        session_instance.client.return_value.list_buckets.return_value = {}

        sgs_data = mock_list_security_groups.return_value
        security_groups = [SecurityGroup(
            account=Account('123456789012'),
            region='eu-west-1',
            id=sg_data['GroupId'],
            name=sg_data['GroupName'],
            owner_id=sg_data['OwnerId'],
            vpc_id=sg_data['VpcId'],
            ip_permissions=[IPPermission(
                from_port=sg_data['IpPermissions'][0]['FromPort'],
                to_port=sg_data['IpPermissions'][0]['ToPort'],
                ip_protocol=sg_data['IpPermissions'][0]['IpProtocol'],
                ip_ranges=[IPRange(
                    cidr_ip=sg_data['IpPermissions'][0]['IpRanges'][0]['CidrIp'],
                    description=sg_data['IpPermissions'][0]['IpRanges'][0]['Description']
                )],
                ipv6_ranges=[IPv6Range(
                    cidr_ipv6=sg_data['IpPermissions'][0]['Ipv6Ranges'][0]['CidrIpv6'],
                    description=sg_data['IpPermissions'][0]['Ipv6Ranges'][0]['Description']
                )],
                prefix_lists=[PrefixList(
                    id=sg_data['IpPermissions'][0]['PrefixListIds'][0]['PrefixListId'],
                    description=sg_data['IpPermissions'][0]['PrefixListIds'][0]['Description']
                )],
                user_id_group_pairs=[UserIDGroupPair(
                    id=sg_data['IpPermissions'][0]['UserIdGroupPairs'][0]['GroupId'],
                    name=sg_data['IpPermissions'][0]['UserIdGroupPairs'][0]['GroupName'],
                    status=sg_data['IpPermissions'][0]['UserIdGroupPairs'][0]['PeeringStatus'],
                    user_id=sg_data['IpPermissions'][0]['UserIdGroupPairs'][0]['UserId'],
                    vpc_id=sg_data['IpPermissions'][0]['UserIdGroupPairs'][0]['VpcId'],
                    description=sg_data['IpPermissions'][0]['UserIdGroupPairs'][0]['Description'],
                    vpc_peering_connection_id=(
                        sg_data['IpPermissions'][0]['UserIdGroupPairs'][0]['VpcPeeringConnectionId']
                    )
                )]
            )]
        ) for sg_data in sgs_data]
        self.security_group.search_security_groups = mock.Mock(return_value=security_groups)

        result = self.security_group.search_security_groups(condition=OR, name='AppSecurityGroup', id='sg-abcdef123456')

        self.assertEqual(result[0].name, 'AppSecurityGroup')
        self.assertIsNotNone(result[0].ip_permissions)
        self.assertEqual(result[0].ip_permissions[0].from_port, 80)
        self.assertEqual(result[0].ip_permissions[0].ip_ranges[0].cidr_ip, '0.0.0.0/0')
        self.assertEqual(result[0].ip_permissions[0].ipv6_ranges[0].cidr_ipv6, '::/0')
        self.assertEqual(result[0].ip_permissions[0].prefix_lists[0].id, 'pl-12345abcde')
        self.assertEqual(result[0].ip_permissions[0].user_id_group_pairs[0].id, 'sg-67890fghij')
        self.assertIsNone(result[0].ip_permissions_egress)
        self.assertIsNone(result[0].tags)

    @patch('boto3.Session')
    @patch('pyawsopstoolkit.session.Session.get_session')
    @patch('pyawsopstoolkit_advsearch.ec2._list_security_groups', return_value=[{
        'Description': 'Main security group for the application',
        'GroupName': 'AppSecurityGroup',
        'OwnerId': '123456789012',
        'GroupId': 'sg-abcdef123456',
        'IpPermissionsEgress': [
            {
                'FromPort': 80,
                'IpProtocol': 'tcp',
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0',
                        'Description': 'Allow all traffic from IPv4'
                    }
                ],
                'Ipv6Ranges': [
                    {
                        'CidrIpv6': '::/0',
                        'Description': 'Allow all traffic from IPv6'
                    }
                ],
                'PrefixListIds': [
                    {
                        'Description': 'Allow traffic from prefix list',
                        'PrefixListId': 'pl-12345abcde'
                    }
                ],
                'ToPort': 80,
                'UserIdGroupPairs': [
                    {
                        'Description': 'Allow traffic from admin security group',
                        'GroupId': 'sg-67890fghij',
                        'GroupName': 'AdminSecurityGroup',
                        'PeeringStatus': 'active',
                        'UserId': '123456789012',
                        'VpcId': 'vpc-abcde12345',
                        'VpcPeeringConnectionId': 'pcx-abc123de'
                    }
                ]
            }
        ],
        'VpcId': 'vpc-12345abcde'
    }])
    @patch('pyawsopstoolkit_advsearch.__validations__._validate_type', return_value=None)
    def test_search_security_groups_with_ip_permissions_egress(
            self, mock_validation, mock_list_security_groups, mock_get_session, mock_session
    ):
        from pyawsopstoolkit.account import Account
        from pyawsopstoolkit_models.ec2.security_group import SecurityGroup, IPPermission, IPRange, IPv6Range, \
            PrefixList, UserIDGroupPair

        mock_client = MagicMock()
        mock_caller_identity = MagicMock()

        mock_caller_identity.get.return_value = '123456789012'
        mock_client.get_caller_identity.return_value = mock_caller_identity
        mock_get_session.return_value.client.return_value = mock_client

        session_instance = mock_session.return_value
        session_instance.client.return_value.list_buckets.return_value = {}

        sgs_data = mock_list_security_groups.return_value
        security_groups = [SecurityGroup(
            account=Account('123456789012'),
            region='eu-west-1',
            id=sg_data['GroupId'],
            name=sg_data['GroupName'],
            owner_id=sg_data['OwnerId'],
            vpc_id=sg_data['VpcId'],
            ip_permissions_egress=[IPPermission(
                from_port=sg_data['IpPermissionsEgress'][0]['FromPort'],
                to_port=sg_data['IpPermissionsEgress'][0]['ToPort'],
                ip_protocol=sg_data['IpPermissionsEgress'][0]['IpProtocol'],
                ip_ranges=[IPRange(
                    cidr_ip=sg_data['IpPermissionsEgress'][0]['IpRanges'][0]['CidrIp'],
                    description=sg_data['IpPermissionsEgress'][0]['IpRanges'][0]['Description']
                )],
                ipv6_ranges=[IPv6Range(
                    cidr_ipv6=sg_data['IpPermissionsEgress'][0]['Ipv6Ranges'][0]['CidrIpv6'],
                    description=sg_data['IpPermissionsEgress'][0]['Ipv6Ranges'][0]['Description']
                )],
                prefix_lists=[PrefixList(
                    id=sg_data['IpPermissionsEgress'][0]['PrefixListIds'][0]['PrefixListId'],
                    description=sg_data['IpPermissionsEgress'][0]['PrefixListIds'][0]['Description']
                )],
                user_id_group_pairs=[UserIDGroupPair(
                    id=sg_data['IpPermissionsEgress'][0]['UserIdGroupPairs'][0]['GroupId'],
                    name=sg_data['IpPermissionsEgress'][0]['UserIdGroupPairs'][0]['GroupName'],
                    status=sg_data['IpPermissionsEgress'][0]['UserIdGroupPairs'][0]['PeeringStatus'],
                    user_id=sg_data['IpPermissionsEgress'][0]['UserIdGroupPairs'][0]['UserId'],
                    vpc_id=sg_data['IpPermissionsEgress'][0]['UserIdGroupPairs'][0]['VpcId'],
                    description=sg_data['IpPermissionsEgress'][0]['UserIdGroupPairs'][0]['Description'],
                    vpc_peering_connection_id=(
                        sg_data['IpPermissionsEgress'][0]['UserIdGroupPairs'][0]['VpcPeeringConnectionId']
                    )
                )]
            )]
        ) for sg_data in sgs_data]
        self.security_group.search_security_groups = mock.Mock(return_value=security_groups)

        result = self.security_group.search_security_groups(condition=OR, name='AppSecurityGroup', id='sg-abcdef123456')

        self.assertEqual(result[0].name, 'AppSecurityGroup')
        self.assertIsNone(result[0].ip_permissions)
        self.assertIsNotNone(result[0].ip_permissions_egress)
        self.assertEqual(result[0].ip_permissions_egress[0].from_port, 80)
        self.assertEqual(result[0].ip_permissions_egress[0].ip_ranges[0].cidr_ip, '0.0.0.0/0')
        self.assertEqual(result[0].ip_permissions_egress[0].ipv6_ranges[0].cidr_ipv6, '::/0')
        self.assertEqual(result[0].ip_permissions_egress[0].prefix_lists[0].id, 'pl-12345abcde')
        self.assertEqual(result[0].ip_permissions_egress[0].user_id_group_pairs[0].id, 'sg-67890fghij')
        self.assertIsNone(result[0].tags)

    @patch('boto3.Session')
    @patch('pyawsopstoolkit.session.Session.get_session')
    @patch('pyawsopstoolkit_advsearch.ec2._list_security_groups', return_value=[{
        'Description': 'Main security group for the application',
        'GroupName': 'AppSecurityGroup',
        'OwnerId': '123456789012',
        'GroupId': 'sg-abcdef123456',
        'Tags': [
            {
                'Key': 'Name',
                'Value': 'AppSecurityGroup'
            },
            {
                'Key': 'Environment',
                'Value': 'Production'
            }
        ],
        'VpcId': 'vpc-12345abcde'
    }])
    @patch('pyawsopstoolkit_advsearch.__validations__._validate_type', return_value=None)
    def test_search_security_groups_with_tags(
            self, mock_validation, mock_list_security_groups, mock_get_session, mock_session
    ):
        from pyawsopstoolkit.account import Account
        from pyawsopstoolkit_models.ec2.security_group import SecurityGroup

        mock_client = MagicMock()
        mock_caller_identity = MagicMock()

        mock_caller_identity.get.return_value = '123456789012'
        mock_client.get_caller_identity.return_value = mock_caller_identity
        mock_get_session.return_value.client.return_value = mock_client

        session_instance = mock_session.return_value
        session_instance.client.return_value.list_buckets.return_value = {}

        sgs_data = mock_list_security_groups.return_value
        security_groups = [SecurityGroup(
            account=Account('123456789012'),
            region='eu-west-1',
            id=sg_data['GroupId'],
            name=sg_data['GroupName'],
            owner_id=sg_data['OwnerId'],
            vpc_id=sg_data['VpcId'],
            tags=sg_data.get('Tags')
        ) for sg_data in sgs_data]
        self.security_group.search_security_groups = mock.Mock(return_value=security_groups)

        result = self.security_group.search_security_groups(
            condition=OR, name='AppSecurityGroup', id='sg-abcdef123456', tag_key='Environment'
        )

        self.assertEqual(result[0].name, 'AppSecurityGroup')
        self.assertIsNone(result[0].ip_permissions)
        self.assertIsNone(result[0].ip_permissions_egress)
        self.assertEqual(result[0].tags[0].get('Key'), 'Name')
        self.assertEqual(result[0].tags[1].get('Key'), 'Environment')


if __name__ == "__main__":
    unittest.main()
