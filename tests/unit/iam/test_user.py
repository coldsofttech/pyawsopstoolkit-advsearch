import unittest
from datetime import datetime
from unittest import mock
from unittest.mock import patch, MagicMock

from pyawsopstoolkit_advsearch import OR, BETWEEN
from pyawsopstoolkit_advsearch.exceptions import SearchAttributeError
from pyawsopstoolkit_advsearch.iam import User


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        from pyawsopstoolkit.session import Session

        self.profile_name = 'temp'
        self.session = Session(profile_name=self.profile_name)
        self.user = User(session=self.session)

    def test_initialization(self):
        self.assertEqual(self.user.session, self.session)

    def test_setters(self):
        from pyawsopstoolkit.session import Session

        new_session = Session(profile_name='sample')
        self.user.session = new_session
        self.assertEqual(self.user.session, new_session)

    def test_invalid_types(self):
        invalid_session = 123

        with self.assertRaises(TypeError):
            User(session=invalid_session)
        with self.assertRaises(TypeError):
            self.user.session = invalid_session

    @patch('boto3.Session')
    def test_search_users_empty_kwargs(self, mock_session):
        session_instance = mock_session.return_value
        session_instance.client.return_value.list_buckets.return_value = {}

        self.assertEqual(len(self.user.search_users()), 0)

    @patch('boto3.Session')
    def test_search_users_all_none(self, mock_session):
        session_instance = mock_session.return_value
        session_instance.client.return_value.list_buckets.return_value = {}

        self.assertEqual(
            len(self.user.search_users(condition=OR, name=None, id=None, arn=None)), 0
        )

    @patch('boto3.Session')
    @patch('pyawsopstoolkit.session.Session.get_session')
    @patch('pyawsopstoolkit_advsearch.iam._list_users', return_value=[{
        'Path': '/',
        'UserName': 'test_user',
        'UserId': 'AID2MAB8DPLSRHEXAMPLE',
        'Arn': 'arn:aws:iam::123456789012:user/test_user',
        'CreateDate': datetime(2022, 5, 18)
    }])
    @patch('pyawsopstoolkit_advsearch.__validations__._validate_type', return_value=None)
    @patch('pyawsopstoolkit_validators.arn_validator.arn', return_value=True)
    @patch('pyawsopstoolkit_validators.region_validator.region', return_value=True)
    def test_search_users_basic(
            self, mock_region, mock_arn, mock_validation, mock_list_users, mock_get_session, mock_session
    ):
        from pyawsopstoolkit.account import Account
        from pyawsopstoolkit_models.iam.user import User

        mock_client = MagicMock()
        mock_caller_identity = MagicMock()

        mock_caller_identity.get.return_value = '123456789012'
        mock_client.get_caller_identity.return_value = mock_caller_identity
        mock_get_session.return_value.client.return_value = mock_client

        session_instance = mock_session.return_value
        session_instance.client.return_value.list_buckets.return_value = {}

        users_data = mock_list_users.return_value
        users = [User(
            account=Account('123456789012'),
            name=user_data['UserName'],
            id=user_data['UserId'],
            arn=user_data['Arn'],
            path=user_data['Path'],
            created_date=user_data.get('CreateDate'),
            password_last_used_date=None,
            permissions_boundary=None,
            tags=None
        ) for user_data in users_data]
        self.user.search_users = mock.Mock(return_value=users)

        result = self.user.search_users(condition=OR, name='test_user', id='AID2MAB8DPLSRHEXAMPLE')

        self.assertEqual(result[0].name, 'test_user')
        self.assertIsNone(result[0].permissions_boundary)
        self.assertIsNone(result[0].password_last_used_date)
        self.assertIsNone(result[0].tags)

    @patch('boto3.Session')
    @patch('pyawsopstoolkit.session.Session.get_session')
    @patch('pyawsopstoolkit_advsearch.iam._list_users', return_value=[{
        'Path': '/',
        'UserName': 'test_user',
        'UserId': 'AID2MAB8DPLSRHEXAMPLE',
        'Arn': 'arn:aws:iam::123456789012:user/test_user',
        'CreateDate': datetime(2022, 5, 18)
    }])
    @patch('pyawsopstoolkit_advsearch.iam._get_user', return_value={
        'Path': '/',
        'UserName': 'test_user',
        'UserId': 'AID2MAB8DPLSRHEXAMPLE',
        'Arn': 'arn:aws:iam::123456789012:user/test_user',
        'CreateDate': datetime(2022, 5, 18),
        'PermissionsBoundary': {
            'PermissionsBoundaryType': 'Managed',
            'PermissionsBoundaryArn': 'arn:aws:iam::123456789012:policy/ManagedPolicy'
        }
    })
    @patch('pyawsopstoolkit_advsearch.__validations__._validate_type', return_value=None)
    @patch('pyawsopstoolkit_validators.arn_validator.arn', return_value=True)
    @patch('pyawsopstoolkit_validators.region_validator.region', return_value=True)
    def test_search_users_with_permissions_boundary(
            self, mock_region, mock_arn, mock_validation, mock_get_user, mock_list_users, mock_get_session, mock_session
    ):
        from pyawsopstoolkit.account import Account
        from pyawsopstoolkit_models.iam.user import User
        from pyawsopstoolkit_models.iam.permissions_boundary import PermissionsBoundary

        mock_client = MagicMock()
        mock_caller_identity = MagicMock()

        mock_caller_identity.get.return_value = '123456789012'
        mock_client.get_caller_identity.return_value = mock_caller_identity
        mock_get_session.return_value.client.return_value = mock_client

        session_instance = mock_session.return_value
        session_instance.client.return_value.list_buckets.return_value = {}

        users_data = mock_get_user.return_value
        users = [User(
            account=Account('123456789012'),
            name=user_data['UserName'],
            id=user_data['UserId'],
            arn=user_data['Arn'],
            path=user_data['Path'],
            created_date=user_data.get('CreateDate'),
            password_last_used_date=None,
            permissions_boundary=PermissionsBoundary(
                type=user_data['PermissionsBoundary']['PermissionsBoundaryType'],
                arn=user_data['PermissionsBoundary']['PermissionsBoundaryArn']
            ),
            tags=None
        ) for user_data in [users_data]]
        self.user.search_users = mock.Mock(return_value=users)

        result = self.user.search_users(
            condition=OR,
            include_details=True,
            name='test_user',
            id='AID2MAB8DPLSRHEXAMPLE',
            permissions_boundary_arn='arn:aws:iam::123456789012:policy/ManagedPolicy'
        )

        self.assertEqual(result[0].name, 'test_user')
        self.assertEqual(result[0].permissions_boundary.arn, 'arn:aws:iam::123456789012:policy/ManagedPolicy')

    @patch('boto3.Session')
    @patch('pyawsopstoolkit.session.Session.get_session')
    def test_search_users_with_permissions_boundary_without_details(self, mock_get_session, mock_session):
        mock_client = MagicMock()
        mock_caller_identity = MagicMock()

        mock_caller_identity.get.return_value = '123456789012'
        mock_client.get_caller_identity.return_value = mock_caller_identity
        mock_get_session.return_value.client.return_value = mock_client

        session_instance = mock_session.return_value
        session_instance.client.return_value.list_buckets.return_value = {}

        with self.assertRaises(SearchAttributeError):
            self.user.search_users(
                condition=OR,
                name='test_user',
                id='AID2MAB8DPLSRHEXAMPLE',
                permissions_boundary_arn='arn:aws:iam::123456789012:policy/ManagedPolicy'
            )

    @patch('boto3.Session')
    @patch('pyawsopstoolkit.session.Session.get_session')
    @patch('pyawsopstoolkit_advsearch.iam._list_users', return_value=[{
        'Path': '/',
        'UserName': 'test_user',
        'UserId': 'AID2MAB8DPLSRHEXAMPLE',
        'Arn': 'arn:aws:iam::123456789012:user/test_user',
        'CreateDate': datetime(2022, 5, 18)
    }])
    @patch('pyawsopstoolkit_advsearch.iam._get_user', return_value={
        'Path': '/',
        'UserName': 'test_user',
        'UserId': 'AID2MAB8DPLSRHEXAMPLE',
        'Arn': 'arn:aws:iam::123456789012:user/test_user',
        'CreateDate': datetime(2022, 5, 18),
        'PermissionsBoundary': {
            'PermissionsBoundaryType': 'Managed',
            'PermissionsBoundaryArn': 'arn:aws:iam::123456789012:policy/ManagedPolicy'
        },
        'Tags': [{'Key': 'test_key', 'Value': 'test_value'}]
    })
    @patch('pyawsopstoolkit_advsearch.__validations__._validate_type', return_value=None)
    @patch('pyawsopstoolkit_validators.arn_validator.arn', return_value=True)
    @patch('pyawsopstoolkit_validators.region_validator.region', return_value=True)
    def test_search_users_with_tags(
            self, mock_region, mock_arn, mock_validation, mock_get_user, mock_list_users, mock_get_session, mock_session
    ):
        from pyawsopstoolkit.account import Account
        from pyawsopstoolkit_models.iam.user import User
        from pyawsopstoolkit_models.iam.permissions_boundary import PermissionsBoundary

        mock_client = MagicMock()
        mock_caller_identity = MagicMock()

        mock_caller_identity.get.return_value = '123456789012'
        mock_client.get_caller_identity.return_value = mock_caller_identity
        mock_get_session.return_value.client.return_value = mock_client

        session_instance = mock_session.return_value
        session_instance.client.return_value.list_buckets.return_value = {}

        users_data = mock_get_user.return_value
        users = [User(
            account=Account('123456789012'),
            name=user_data['UserName'],
            id=user_data['UserId'],
            arn=user_data['Arn'],
            path=user_data['Path'],
            created_date=user_data.get('CreateDate'),
            password_last_used_date=None,
            permissions_boundary=PermissionsBoundary(
                type=user_data['PermissionsBoundary']['PermissionsBoundaryType'],
                arn=user_data['PermissionsBoundary']['PermissionsBoundaryArn']
            ),
            tags=user_data.get('Tags')
        ) for user_data in [users_data]]
        self.user.search_users = mock.Mock(return_value=users)

        result = self.user.search_users(
            condition=OR, include_details=True, name='test_user', id='AID2MAB8DPLSRHEXAMPLE', tag_key='test_key'
        )

        self.assertEqual(result[0].name, 'test_user')
        self.assertEqual(result[0].tags[0].get('Key'), 'test_key')

    @patch('boto3.Session')
    @patch('pyawsopstoolkit.session.Session.get_session')
    def test_search_users_with_tags_without_include(self, mock_get_session, mock_session):
        mock_client = MagicMock()
        mock_caller_identity = MagicMock()

        mock_caller_identity.get.return_value = '123456789012'
        mock_client.get_caller_identity.return_value = mock_caller_identity
        mock_get_session.return_value.client.return_value = mock_client

        session_instance = mock_session.return_value
        session_instance.client.return_value.list_buckets.return_value = {}

        with self.assertRaises(SearchAttributeError):
            self.user.search_users(condition=OR, name='test_user', id='AID2MAB8DPLSRHEXAMPLE', tag_key='test_key')

    @patch('boto3.Session')
    @patch('pyawsopstoolkit.session.Session.get_session')
    @patch('pyawsopstoolkit_advsearch.iam._list_users', return_value=[{
        'Path': '/',
        'UserName': 'test_user',
        'UserId': 'AID2MAB8DPLSRHEXAMPLE',
        'Arn': 'arn:aws:iam::123456789012:user/test_user',
        'CreateDate': datetime(2022, 5, 18)
    }])
    @patch('pyawsopstoolkit_advsearch.iam._get_user', return_value={
        'Path': '/',
        'UserName': 'test_user',
        'UserId': 'AID2MAB8DPLSRHEXAMPLE',
        'Arn': 'arn:aws:iam::123456789012:user/test_user',
        'CreateDate': datetime(2022, 5, 18),
        'PermissionsBoundary': {
            'PermissionsBoundaryType': 'Managed',
            'PermissionsBoundaryArn': 'arn:aws:iam::123456789012:policy/ManagedPolicy'
        }
    })
    @patch('pyawsopstoolkit_advsearch.iam._get_login_profile', return_value={
        'UserName': 'test_user',
        'CreateDate': datetime(2022, 6, 18)
    })
    @patch('pyawsopstoolkit_advsearch.__validations__._validate_type', return_value=None)
    @patch('pyawsopstoolkit_validators.arn_validator.arn', return_value=True)
    @patch('pyawsopstoolkit_validators.region_validator.region', return_value=True)
    def test_search_users_with_login_profile(
            self, mock_region, mock_arn, mock_validation, mock_get_login_profile, mock_get_user, mock_list_users,
            mock_get_session, mock_session
    ):
        from pyawsopstoolkit.account import Account
        from pyawsopstoolkit_models.iam.user import User, LoginProfile
        from pyawsopstoolkit_models.iam.permissions_boundary import PermissionsBoundary

        mock_client = MagicMock()
        mock_caller_identity = MagicMock()

        mock_caller_identity.get.return_value = '123456789012'
        mock_client.get_caller_identity.return_value = mock_caller_identity
        mock_get_session.return_value.client.return_value = mock_client

        session_instance = mock_session.return_value
        session_instance.client.return_value.list_buckets.return_value = {}

        users_data = mock_get_user.return_value
        login_profile_data = mock_get_login_profile.return_value
        users = [User(
            account=Account('123456789012'),
            name=user_data['UserName'],
            id=user_data['UserId'],
            arn=user_data['Arn'],
            path=user_data['Path'],
            created_date=user_data.get('CreateDate'),
            password_last_used_date=None,
            permissions_boundary=PermissionsBoundary(
                type=user_data['PermissionsBoundary']['PermissionsBoundaryType'],
                arn=user_data['PermissionsBoundary']['PermissionsBoundaryArn']
            ),
            login_profile=LoginProfile(
                created_date=login_profile_data.get('CreateDate')
            ),
            tags=None
        ) for user_data in [users_data]]
        self.user.search_users = mock.Mock(return_value=users)

        result = self.user.search_users(
            condition=OR,
            include_details=True,
            name='test_user',
            id='AID2MAB8DPLSRHEXAMPLE',
            login_profile_created_date={BETWEEN: [datetime(2021, 6, 18), datetime(2023, 6, 18)]}
        )

        self.assertEqual(result[0].name, 'test_user')
        self.assertEqual(result[0].login_profile.created_date, datetime(2022, 6, 18))

    @patch('boto3.Session')
    @patch('pyawsopstoolkit.session.Session.get_session')
    def test_search_users_with_login_profile_without_details(self, mock_get_session, mock_session):
        mock_client = MagicMock()
        mock_caller_identity = MagicMock()

        mock_caller_identity.get.return_value = '123456789012'
        mock_client.get_caller_identity.return_value = mock_caller_identity
        mock_get_session.return_value.client.return_value = mock_client

        session_instance = mock_session.return_value
        session_instance.client.return_value.list_buckets.return_value = {}

        with self.assertRaises(SearchAttributeError):
            self.user.search_users(
                condition=OR,
                name='test_user',
                id='AID2MAB8DPLSRHEXAMPLE',
                login_profile_created_date={BETWEEN: [datetime(2021, 6, 18), datetime(2023, 6, 18)]}
            )

    @patch('boto3.Session')
    @patch('pyawsopstoolkit.session.Session.get_session')
    @patch('pyawsopstoolkit_advsearch.iam._list_users', return_value=[{
        'Path': '/',
        'UserName': 'test_user',
        'UserId': 'AID2MAB8DPLSRHEXAMPLE',
        'Arn': 'arn:aws:iam::123456789012:user/test_user',
        'CreateDate': datetime(2022, 5, 18)
    }])
    @patch('pyawsopstoolkit_advsearch.iam._get_user', return_value={
        'Path': '/',
        'UserName': 'test_user',
        'UserId': 'AID2MAB8DPLSRHEXAMPLE',
        'Arn': 'arn:aws:iam::123456789012:user/test_user',
        'CreateDate': datetime(2022, 5, 18),
        'PermissionsBoundary': {
            'PermissionsBoundaryType': 'Managed',
            'PermissionsBoundaryArn': 'arn:aws:iam::123456789012:policy/ManagedPolicy'
        }
    })
    @patch('pyawsopstoolkit_advsearch.iam._get_login_profile', return_value={
        'UserName': 'test_user',
        'CreateDate': datetime(2022, 6, 18)
    })
    @patch('pyawsopstoolkit_advsearch.iam._list_access_keys', return_value=[{
        'UserName': 'test_user',
        'AccessKeyId': 'ACCESSKEY_ID1',
        'Status': 'Active',
        'CreateDate': datetime(2022, 5, 18)
    }])
    @patch('pyawsopstoolkit_advsearch.iam._get_access_key_last_used', return_value={
        'UserName': 'test_user',
        'AccessKeyLastUsed': {
            'LastUsedDate': datetime(2022, 6, 18),
            'ServiceName': 'ec2.amazonaws.com'
        }
    })
    @patch('pyawsopstoolkit_advsearch.__validations__._validate_type', return_value=None)
    @patch('pyawsopstoolkit_validators.arn_validator.arn', return_value=True)
    @patch('pyawsopstoolkit_validators.region_validator.region', return_value=True)
    def test_search_users_with_access_keys(
            self, mock_region, mock_arn, mock_validation, mock_get_access_key_last_used, mock_list_access_keys,
            mock_get_login_profile, mock_get_user, mock_list_users, mock_get_session, mock_session
    ):
        from pyawsopstoolkit.account import Account
        from pyawsopstoolkit_models.iam.user import User, LoginProfile, AccessKey
        from pyawsopstoolkit_models.iam.permissions_boundary import PermissionsBoundary

        mock_client = MagicMock()
        mock_caller_identity = MagicMock()

        mock_caller_identity.get.return_value = '123456789012'
        mock_client.get_caller_identity.return_value = mock_caller_identity
        mock_get_session.return_value.client.return_value = mock_client

        session_instance = mock_session.return_value
        session_instance.client.return_value.list_buckets.return_value = {}

        users_data = mock_get_user.return_value
        login_profile_data = mock_get_login_profile.return_value
        access_keys = mock_list_access_keys.return_value
        access_key_data = mock_get_access_key_last_used.return_value
        users = [User(
            account=Account('123456789012'),
            name=user_data['UserName'],
            id=user_data['UserId'],
            arn=user_data['Arn'],
            path=user_data['Path'],
            created_date=user_data.get('CreateDate'),
            password_last_used_date=None,
            permissions_boundary=PermissionsBoundary(
                type=user_data['PermissionsBoundary']['PermissionsBoundaryType'],
                arn=user_data['PermissionsBoundary']['PermissionsBoundaryArn']
            ),
            login_profile=LoginProfile(
                created_date=login_profile_data.get('CreateDate')
            ),
            access_keys=[AccessKey(
                id=a_key.get('AccessKeyId', ''),
                status=a_key.get('Status', ''),
                created_date=a_key.get('CreateDate', None),
                last_used_date=access_key_data.get('AccessKeyLastUsed', {}).get('LastUsedDate', None),
                last_used_service=access_key_data.get('AccessKeyLastUsed', {}).get('ServiceName', None)
            ) for a_key in access_keys],
            tags=None
        ) for user_data in [users_data]]
        self.user.search_users = mock.Mock(return_value=users)

        result = self.user.search_users(
            condition=OR,
            include_details=True,
            name='test_user',
            id='AID2MAB8DPLSRHEXAMPLE',
            access_key_service='ec2.amazonaws.com'
        )

        self.assertEqual(result[0].name, 'test_user')
        self.assertEqual(result[0].access_keys[0].last_used_service, 'ec2.amazonaws.com')

    @patch('boto3.Session')
    @patch('pyawsopstoolkit.session.Session.get_session')
    def test_search_users_with_access_keys_without_details(self, mock_get_session, mock_session):
        mock_client = MagicMock()
        mock_caller_identity = MagicMock()

        mock_caller_identity.get.return_value = '123456789012'
        mock_client.get_caller_identity.return_value = mock_caller_identity
        mock_get_session.return_value.client.return_value = mock_client

        session_instance = mock_session.return_value
        session_instance.client.return_value.list_buckets.return_value = {}

        with self.assertRaises(SearchAttributeError):
            self.user.search_users(
                condition=OR,
                name='test_user',
                id='AID2MAB8DPLSRHEXAMPLE',
                access_key_service='ec2.amazonaws.com'
            )


if __name__ == "__main__":
    unittest.main()
