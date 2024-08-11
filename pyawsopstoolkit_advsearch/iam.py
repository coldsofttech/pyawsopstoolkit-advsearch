from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pyawsopstoolkit_advsearch.__globals__ import MAX_WORKERS
from pyawsopstoolkit_advsearch.__validations__ import _validate_type
from pyawsopstoolkit_advsearch.exceptions import SearchAttributeError, AdvanceSearchError
from pyawsopstoolkit_advsearch.search import OR, _match_compare_condition, _match_tag_condition, _match_condition, AND

BOTO3_CLIENT = "iam"


def _get_access_key_last_used(session, access_key_id) -> dict:
    """
    Utilizing boto3 IAM, this method retrieves comprehensive details of IAM user access key last used information
    identified by the specified username. Reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/get_access_key_last_used.html

    :param session: The Session object which provide access to AWS services.
    :type session: pyawsopstoolkit.session.Session
    :param access_key_id: The ID of the IAM user access key.
    :type access_key_id: str
    :return: Details of the IAM user access key last used.
    :rtype: dict
    """
    from botocore.exceptions import ClientError

    try:
        if session.cert_path:
            iam_client = session.get_session().client(BOTO3_CLIENT, verify=session.cert_path)
        else:
            iam_client = session.get_session().client(BOTO3_CLIENT)

        return iam_client.get_access_key_last_used(AccessKeyId=access_key_id)
    except ClientError as e:
        raise e


def _get_login_profile(session, user_name) -> dict:
    """
    Utilizing boto3 IAM, this method retrieves comprehensive details of an IAM user login profile identified
    by the specified username. Reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/get_login_profile.html

    :param session: The Session object which provide access to AWS services.
    :type session: pyawsopstoolkit.session.Session
    :param user_name: The name of the IAM user.
    :type user_name: str
    :return: Details of the IAM user login profile.
    :rtype: dict
    """
    from botocore.exceptions import ClientError

    try:
        if session.cert_path:
            iam_client = session.get_session().client(BOTO3_CLIENT, verify=session.cert_path)
        else:
            iam_client = session.get_session().client(BOTO3_CLIENT)

        return iam_client.get_login_profile(UserName=user_name)
    except ClientError as e:
        raise e


def _get_role(session, role_name) -> dict:
    """
    Utilizing boto3 IAM, this method retrieves comprehensive details of an IAM role identified by the
    specified role name. Reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/get_role.html

    :param session: The Session object which provide access to AWS services.
    :type session: pyawsopstoolkit.session.Session
    :param role_name: The name of the IAM role.
    :type role_name: str
    :return: Details of the IAM role.
    :rtype: dict
    """
    from botocore.exceptions import ClientError

    try:
        if session.cert_path:
            iam_client = session.get_session().client(BOTO3_CLIENT, verify=session.cert_path)
        else:
            iam_client = session.get_session().client(BOTO3_CLIENT)

        return iam_client.get_role(RoleName=role_name)
    except ClientError as e:
        raise e


def _get_user(session, user_name) -> dict:
    """
    Utilizing boto3 IAM, this method retrieves comprehensive details of an IAM user identified by the
    specified username. Reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/get_user.html

    :param session: The Session object which provide access to AWS services.
    :type session: pyawsopstoolkit.session.Session
    :param user_name: The name of the IAM user.
    :type user_name: str
    :return: Details of the IAM user.
    :rtype: dict
    """
    from botocore.exceptions import ClientError

    try:
        if session.cert_path:
            iam_client = session.get_session().client(BOTO3_CLIENT, verify=session.cert_path)
        else:
            iam_client = session.get_session().client(BOTO3_CLIENT)

        return iam_client.get_user(UserName=user_name)
    except ClientError as e:
        raise e


def _list_access_keys(session, user_name) -> list:
    """
    Utilizing boto3 IAM, this method retrieves a list of all access keys associated with IAM user leveraging the
    provided ISession object. Reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAccessKeys.html

    :param session: The Session object which provide access to AWS services.
    :type session: pyawsopstoolkit.session.Session
    :param user_name: The name of the IAM user.
    :type user_name: str
    :return: A list containing IAM user access keys.
    :rtype: list
    """
    from botocore.exceptions import ClientError

    access_keys_to_process = []

    try:
        if session.cert_path:
            iam_client = session.get_session().client(BOTO3_CLIENT, verify=session.cert_path)
        else:
            iam_client = session.get_session().client(BOTO3_CLIENT)
        iam_paginator = iam_client.get_paginator('list_access_keys')

        for page in iam_paginator.paginate(UserName=user_name):
            access_keys_to_process.extend(page.get('AccessKeyMetadata', []))
    except ClientError as e:
        raise e

    return access_keys_to_process


def _list_roles(session) -> list:
    """
    Utilizing boto3 IAM, this method retrieves a list of all roles leveraging the provided ISession object.
    Note: The returned dictionary excludes PermissionsBoundary, LastUsed, and Tags. Reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRoles.html

    :param session: The Session object which provide access to AWS services.
    :type session: pyawsopstoolkit.session.Session
    :return: A list containing IAM roles.
    :rtype: list
    """
    from botocore.exceptions import ClientError

    roles_to_process = []

    try:
        if session.cert_path:
            iam_client = session.get_session().client(BOTO3_CLIENT, verify=session.cert_path)
        else:
            iam_client = session.get_session().client(BOTO3_CLIENT)
        iam_paginator = iam_client.get_paginator('list_roles')

        for page in iam_paginator.paginate():
            roles_to_process.extend(page.get('Roles', []))
    except ClientError as e:
        raise e

    return roles_to_process


def _list_users(session) -> list:
    """
    Utilizing boto3 IAM, this method retrieves a list of all users leveraging the provided ISession object.
    Note: The returned dictionary excludes PermissionsBoundary and Tags. Reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUsers.html

    :param session: The Session object which provide access to AWS services.
    :type session: pyawsopstoolkit.session.Session
    :return: A list containing IAM users.
    :rtype: list
    """
    from botocore.exceptions import ClientError

    users_to_process = []

    try:
        if session.cert_path:
            iam_client = session.get_session().client(BOTO3_CLIENT, verify=session.cert_path)
        else:
            iam_client = session.get_session().client(BOTO3_CLIENT)
        iam_paginator = iam_client.get_paginator('list_users')

        for page in iam_paginator.paginate():
            users_to_process.extend(page.get('Users', []))
    except ClientError as e:
        raise e

    return users_to_process


@dataclass
class Role:
    """
    A class representing advance search features related with IAM roles.
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
    def _convert_to_iam_role(account: Account, role: dict):
        """
        This function transforms the dictionary response from boto3 IAM into a format compatible with the AWS Ops
        Toolkit, adhering to the pyawsopstoolkit_models structure. Additionally, it incorporates account-related
        summary information into the IAM role details.

        :param account: An Account object containing AWS account information.
        :type account: pyawsopstoolkit.account.Account
        :param role: The boto3 IAM service response for an IAM role.
        :type role: dict
        :return: An AWS Ops Toolkit compatible object containing all IAM role details.
        :rtype: pyawsopstoolkit_models.iam.role.Role
        """
        from pyawsopstoolkit_models.iam.role import LastUsed, Role
        from pyawsopstoolkit_models.iam.permissions_boundary import PermissionsBoundary

        iam_role = Role(
            account=account,
            name=role.get('RoleName', ''),
            id=role.get('RoleId', ''),
            arn=role.get('Arn', ''),
            max_session_duration=role.get('MaxSessionDuration', 0),
            path=role.get('Path', ''),
            created_date=role.get('CreateDate', None),
            assume_role_policy_document=role.get('AssumeRolePolicyDocument', None),
            description=role.get('Description', None)
        )

        boundary = role.get('PermissionsBoundary', {})
        if boundary:
            iam_role.permissions_boundary = PermissionsBoundary(
                type=boundary.get('PermissionsBoundaryType', ''),
                arn=boundary.get('PermissionsBoundaryArn', '')
            )

        last_used = role.get('RoleLastUsed')
        if last_used:
            iam_role.last_used = LastUsed(
                used_date=last_used.get('LastUsedDate', None),
                region=last_used.get('Region', None)
            )

        iam_role.tags = role.get('Tags', [])

        return iam_role

    def search_roles(
            self,
            condition: str = OR,
            include_details: bool = False,
            **kwargs
    ) -> list:
        """
        Returns a list of IAM roles using advanced search features supported by the specified arguments. For details on
        supported kwargs, please refer to the readme document.

        :param condition: The condition to be applied: 'OR' or 'AND'.
        :type condition: str
        :param include_details: Flag to indicate to include additional details of the IAM role.
        This includes information about permissions boundary, last used, and tags. Default is False.
        :type include_details: bool
        :param kwargs: Key-based arguments defining search criteria.
        :return: A list of IAM roles.
        :rtype: list
        """
        _validate_type(condition, str, 'condition should be a string and should be either "OR" or "AND".')
        _validate_type(include_details, bool, 'include_details should be a boolean.')

        def _process_role(role_detail):
            if include_details:
                role_detail = _get_role(self.session, role_detail.get('RoleName', '')).get('Role', {})

            return self._convert_to_iam_role(self.session.get_account(), role_detail)

        def _match_role(role_detail):
            if role_detail:
                matched = False if condition == OR else True
                for key, value in kwargs.items():
                    if value is not None:
                        role_field = ''
                        if key.lower() == 'path':
                            role_field = role_detail.get('Path', '')
                        elif key.lower() == 'name':
                            role_field = role_detail.get('RoleName', '')
                        elif key.lower() == 'id':
                            role_field = role_detail.get('RoleId', '')
                        elif key.lower() == 'arn':
                            role_field = role_detail.get('Arn', '')
                        elif key.lower() == 'description':
                            role_field = role_detail.get('Description', '')
                        elif key.lower() == 'permissions_boundary_type':
                            if include_details:
                                role_detail = _get_role(self.session, role_detail.get('RoleName', '')).get('Role', {})
                                _permissions_boundary = role_detail.get('PermissionsBoundary', {})
                                role_field = _permissions_boundary.get('PermissionsBoundaryType', '')
                        elif key.lower() == 'permissions_boundary_arn':
                            if include_details:
                                role_detail = _get_role(self.session, role_detail.get('RoleName', '')).get('Role', {})
                                _permissions_boundary = role_detail.get('PermissionsBoundary', {})
                                role_field = _permissions_boundary.get('PermissionsBoundaryArn', '')
                        elif key.lower() == 'max_session_duration':
                            role_field = role_detail.get('MaxSessionDuration', 0)
                            matched = _match_compare_condition(value, role_field, condition, matched)
                        elif key.lower() == 'created_date':
                            role_field = role_detail.get('CreateDate', None)
                            if isinstance(role_field, datetime):
                                role_field = role_field.replace(tzinfo=None)
                                matched = _match_compare_condition(value, role_field, condition, matched)
                        elif key.lower() == 'last_used_date':
                            if include_details:
                                role_detail = _get_role(self.session, role_detail.get('RoleName', '')).get('Role', {})
                                _last_used = role_detail.get('RoleLastUsed', {})
                                role_field = _last_used.get('LastUsedDate', None)
                                if isinstance(role_field, datetime):
                                    role_field = role_field.replace(tzinfo=None)
                                    matched = _match_compare_condition(value, role_field, condition, matched)
                        elif key.lower() == 'last_used_region':
                            if include_details:
                                role_detail = _get_role(self.session, role_detail.get('RoleName', '')).get('Role', {})
                                _last_used = role_detail.get('RoleLastUsed', {})
                                role_field = _last_used.get('Region', '')
                        elif key.lower() == 'tag_key':
                            if include_details:
                                role_detail = _get_role(self.session, role_detail.get('RoleName', '')).get('Role', {})
                                tags = {tag['Key']: tag['Value'] for tag in role_detail.get('Tags', [])}
                                matched = _match_tag_condition(value, tags, condition, matched, key_only=True)
                        elif key.lower() == 'tag':
                            if include_details:
                                role_detail = _get_role(self.session, role_detail.get('RoleName', '')).get('Role', {})
                                tags = {tag['Key']: tag['Value'] for tag in role_detail.get('Tags', [])}
                                matched = _match_tag_condition(value, tags, condition, matched, key_only=False)

                        if key.lower() not in [
                            'max_session_duration', 'created_date', 'last_used_date', 'tag_key', 'tag'
                        ]:
                            matched = _match_condition(value, role_field, condition, matched)

                        if (condition == OR and matched) or (condition == AND and not matched):
                            break

                if matched:
                    return _process_role(role_detail)

        roles_to_return = []

        from botocore.exceptions import ClientError
        try:
            include_details_keys = {
                'permissions_boundary_type',
                'permissions_boundary_arn',
                'last_used_date',
                'last_used_region',
                'tag',
                'tag_key'
            }

            if not include_details and any(k in include_details_keys for k in kwargs):
                raise SearchAttributeError(
                    f'include_details is required for below keys: {", ".join(sorted(include_details_keys))}'
                )

            roles_to_process = _list_roles(self.session)

            if len(kwargs) == 0:
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    future_to_role = {executor.submit(_process_role, role): role for role in roles_to_process}
                    for future in as_completed(future_to_role):
                        role_result = future.result()
                        if role_result is not None:
                            roles_to_return.append(role_result)
            else:
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    future_to_role = {executor.submit(_match_role, role): role for role in roles_to_process}
                    for future in as_completed(future_to_role):
                        role_result = future.result()
                        if role_result is not None:
                            roles_to_return.append(role_result)
        except ClientError as e:
            raise AdvanceSearchError('search_roles', e)

        return roles_to_return


@dataclass
class User:
    """
    A class representing advance search features related with IAM users.
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
    def _convert_to_iam_user(
            account: Account,
            user: dict,
            login_profile: Optional[dict] = None,
            access_keys: Optional[list] = None
    ):
        """
        This function transforms the dictionary response from boto3 IAM into a format compatible with the AWS Ops
        Toolkit, adhering to the pyawsopstoolkit_models structure. Additionally, it incorporates account-related
        summary information into the IAM user details.

        :param account: An Account object containing AWS account information.
        :type account: pyawsopstoolkit.account.Account
        :param user: The boto3 IAM service response for an IAM user.
        :type user: dict
        :param login_profile: The boto3 IAM login profile service response for an IAM user.
        :type login_profile: dict
        :param access_keys: The boto3 IAM access keys service response for an IAM user.
        :type access_keys: list
        :return: An AWS Ops Toolkit compatible object containing all IAM user details.
        :rtype: pyawsopstoolkit_models.iam.user.User
        """
        from pyawsopstoolkit_models.iam.user import AccessKey, LoginProfile, User
        from pyawsopstoolkit_models.iam.permissions_boundary import PermissionsBoundary

        iam_user = User(
            account=account,
            name=user.get('UserName', ''),
            id=user.get('UserId', ''),
            arn=user.get('Arn', ''),
            path=user.get('Path', ''),
            created_date=user.get('CreateDate', None),
            password_last_used_date=user.get('PasswordLastUsed', None)
        )

        boundary = user.get('PermissionsBoundary', {})
        if boundary:
            iam_user.permissions_boundary = PermissionsBoundary(
                type=boundary.get('PermissionsBoundaryType', ''),
                arn=boundary.get('PermissionsBoundaryArn', '')
            )

        if login_profile:
            iam_user.login_profile = LoginProfile(
                created_date=login_profile.get('CreateDate', None),
                password_reset_required=login_profile.get('PasswordResetRequired', False)
            )

        if access_keys:
            iam_user.access_keys = [
                AccessKey(
                    id=key.get('access_key', {}).get('AccessKeyId', ''),
                    status=key.get('access_key', {}).get('Status', ''),
                    created_date=key.get('access_key', {}).get('CreateDate', None),
                    last_used_date=key.get('last_used', {}).get('AccessKeyLastUsed', {}).get('LastUsedDate', None),
                    last_used_service=key.get('last_used', {}).get('AccessKeyLastUsed', {}).get('ServiceName', None),
                    last_used_region=key.get('last_used', {}).get('AccessKeyLastUsed', {}).get('Region', None)
                )
                for key in access_keys
            ]

        iam_user.tags = user.get('Tags', [])

        return iam_user

    def search_users(
            self,
            condition: str = OR,
            include_details: bool = False,
            **kwargs
    ) -> list:
        """
        Returns a list of IAM users using advanced search feature supported by the specified arguments. For details on
        supported kwargs, please refer to the readme document.

        :param condition: The condition to be applied: 'OR' or 'AND'.
        :type condition: str
        :param include_details: Flag to indicate to include additional details of the IAM user.
        This includes information about permissions boundary and tags. Default is False.
        :type include_details: bool
        :param kwargs: Key-based arguments defining search criteria.
        :return: A list of IAM users.
        :rtype: list
        """
        _validate_type(condition, str, 'condition should be a string and should be either "OR" or "AND".')
        _validate_type(include_details, bool, 'include_details should be a boolean.')

        def _process_user(user_detail):
            login_profile_detail = None
            access_keys_detail = []

            if include_details:
                user_detail = _get_user(self.session, user_detail.get('UserName', '')).get('User', {})
                login_profile_detail = _get_login_profile(self.session, user_detail.get('UserName', '')).get(
                    'LoginProfile', {})
                for a_key in _list_access_keys(self.session, user_detail.get('UserName', '')):
                    a_key_last_used = _get_access_key_last_used(self.session, a_key.get('AccessKeyId', ''))
                    access_keys_detail.append({
                        'access_key': a_key,
                        'last_used': a_key_last_used
                    })

            return self._convert_to_iam_user(
                self.session.get_account(), user_detail, login_profile_detail, access_keys_detail
            )

        def _match_user(user_detail):
            if user_detail:
                matched = False if condition == OR else True
                for key, value in kwargs.items():
                    if value is not None:
                        user_field = ''
                        if key.lower() == 'path':
                            user_field = user_detail.get('Path', '')
                        elif key.lower() == 'name':
                            user_field = user_detail.get('UserName', '')
                        elif key.lower() == 'id':
                            user_field = user_detail.get('UserId', '')
                        elif key.lower() == 'arn':
                            user_field = user_detail.get('Arn', '')
                        elif key.lower() == 'created_date':
                            user_field = user_detail.get('CreateDate', None)
                            if isinstance(user_field, datetime):
                                user_field = user_field.replace(tzinfo=None)
                                matched = _match_compare_condition(value, user_field, condition, matched)
                        elif key.lower() == 'password_last_used_date':
                            user_field = user_detail.get('PasswordLastUsed', None)
                            if isinstance(user_field, datetime):
                                user_field = user_field.replace(tzinfo=None)
                                matched = _match_compare_condition(value, user_field, condition, matched)
                        elif key.lower() == 'permissions_boundary_type':
                            if include_details:
                                user_detail = _get_user(self.session, user_detail.get('UserName', '')).get('User', {})
                                _permissions_boundary = user_detail.get('PermissionsBoundary', {})
                                user_field = _permissions_boundary.get('PermissionsBoundaryType', '')
                        elif key.lower() == 'permissions_boundary_arn':
                            if include_details:
                                user_detail = _get_user(self.session, user_detail.get('UserName', '')).get('User', {})
                                _permissions_boundary = user_detail.get('PermissionsBoundary', {})
                                user_field = _permissions_boundary.get('PermissionsBoundaryArn', '')
                        elif key.lower() == 'tag_key':
                            if include_details:
                                user_detail = _get_user(self.session, user_detail.get('UserName', '')).get('User', {})
                                tags = {tag['Key']: tag['Value'] for tag in user_detail.get('Tags', [])}
                                matched = _match_tag_condition(value, tags, condition, matched, key_only=True)
                        elif key.lower() == 'tag':
                            if include_details:
                                user_detail = _get_user(self.session, user_detail.get('UserName', '')).get('User', {})
                                tags = {tag['Key']: tag['Value'] for tag in user_detail.get('Tags', [])}
                                matched = _match_tag_condition(value, tags, condition, matched, key_only=False)
                        elif key.lower() == 'login_profile_created_date':
                            if include_details:
                                login_profile_detail = (
                                    _get_login_profile(self.session, user_detail.get('UserName', '')).get(
                                        'LoginProfile', {})
                                )
                                user_field = login_profile_detail.get('CreateDate', None)
                                if isinstance(user_field, datetime):
                                    user_field = user_field.replace(tzinfo=None)
                                    matched = _match_compare_condition(value, user_field, condition, matched)
                        elif key.lower() == 'login_profile_password_reset_required':
                            if include_details:
                                login_profile_detail = (
                                    _get_login_profile(self.session, user_detail.get('UserName', '')).get(
                                        'LoginProfile', {})
                                )
                                user_field = login_profile_detail.get('PasswordResetRequired', False)
                        elif key.lower() == 'access_key_id':
                            if include_details:
                                user_field = []
                                for access_key in _list_access_keys(self.session, user_detail.get('UserName', '')):
                                    user_field.append(access_key.get('AccessKeyId', ''))
                        elif key.lower() == 'access_key_status':
                            if include_details:
                                user_field = []
                                for access_key in _list_access_keys(self.session, user_detail.get('UserName', '')):
                                    user_field.append(access_key.get('Status', ''))
                        elif key.lower() == 'access_key_service':
                            if include_details:
                                user_field = []
                                for access_key in _list_access_keys(self.session, user_detail.get('UserName', '')):
                                    detail = _get_access_key_last_used(self.session, access_key.get('AccessKeyId', ''))
                                    if detail is not None:
                                        user_field.append(detail.get('AccessKeyLastUsed', {}).get('ServiceName', ''))
                        elif key.lower() == 'access_key_region':
                            if include_details:
                                user_field = []
                                for access_key in _list_access_keys(self.session, user_detail.get('UserName', '')):
                                    detail = _get_access_key_last_used(self.session, access_key.get('AccessKeyId', ''))
                                    if detail is not None:
                                        user_field.append(detail.get('AccessKeyLastUsed', {}).get('Region', ''))

                        if key.lower() not in [
                            'created_date', 'password_last_used_date', 'tag_key', 'tag', 'login_profile_created_date'
                        ]:
                            matched = _match_condition(value, user_field, condition, matched)

                        if (condition == OR and matched) or (condition == AND and not matched):
                            break

                if matched:
                    return _process_user(user_detail)

        users_to_return = []

        from botocore.exceptions import ClientError
        try:
            include_details_keys = {
                'permissions_boundary_type',
                'permissions_boundary_arn',
                'tag',
                'tag_key',
                'login_profile_created_date',
                'login_profile_password_reset_required',
                'access_key_id',
                'access_key_status',
                'access_key_service',
                'access_key_region'
            }

            if not include_details and any(k in include_details_keys for k in kwargs):
                raise SearchAttributeError(
                    f'include_details is required for below keys: {", ".join(sorted(include_details_keys))}'
                )

            users_to_process = _list_users(self.session)

            if len(kwargs) == 0:
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    future_to_user = {executor.submit(_process_user, user): user for user in users_to_process}
                    for future in as_completed(future_to_user):
                        user_result = future.result()
                        if user_result is not None:
                            users_to_return.append(user_result)
            else:
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    future_to_user = {executor.submit(_match_user, user): user for user in users_to_process}
                    for future in as_completed(future_to_user):
                        user_result = future.result()
                        if user_result is not None:
                            users_to_return.append(user_result)
        except ClientError as e:
            raise AdvanceSearchError('search_users', e)

        return users_to_return
