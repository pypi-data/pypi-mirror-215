# from taco_utils.models.graphql import UserPermissions, Balance, AccountInformation, AchDepositWithdrawalRequest


# def get_user_permissions(account_number: str, url: str, api_key: str) -> UserPermissions:
#     """
#     Fetch a user's permissions by account number, should only be one.
#     """
#     user_permissions = list(
#         UserPermissions.account_number_index(
#             url=url,
#             api_key=api_key,
#             account_number=account_number,
#             system_access=None,
#         )
#     )
#     if len(user_permissions) > 0:
#         user_permissions: UserPermissions = user_permissions[0]
#     else:
#         raise Exception(f"No permissions found for account number: {account_number}")

#     return user_permissions

# def get_deposit_withdrawal_by_transfer_id(transfer_id: str, url: str, api_key: str) -> AchDepositWithdrawalRequest:
#     """
#     Fetch a transfer by transferId, should only be one.
#     """
#     ach_deposit_withdrawal = list(
#         AchDepositWithdrawalRequest.transfer_id_index(
#             url=url,
#             api_key=api_key,
#             transfer_id=transfer_id,
#             system_access=None,
#         )
#     )
#     if len(ach_deposit_withdrawal) > 0:
#         ach_deposit_withdrawal: AchDepositWithdrawalRequest = ach_deposit_withdrawal[0]
#     else:
#         raise Exception(f"No transfers found for transfer id: {transfer_id}")

#     return ach_deposit_withdrawal


# def get_balance(account_number: str, url: str, api_key: str) -> Balance:
#     """
#     Fetch a user's balances by account number, should only be one.
#     """
#     balances = list(
#         Balance.account_number_index(
#             url=url,
#             api_key=api_key,
#             account_number=account_number,
#             _id=None,
#         )
#     )
#     if len(balances) > 0:
#         balance: Balance = balances[0]
#     else:
#         raise Exception(f"No balance found for account number: {account_number}")

#     return balance


# def get_account_information(account_number: str, url: str, api_key: str) -> AccountInformation:
#     """
#     Fetch a user's account information by account number, should only be one.
#     """
#     account_information = list(
#         AccountInformation.account_number_index(
#             url=url,
#             api_key=api_key,
#             account_number=account_number,
#             _id=None,
#         )
#     )
#     if len(account_information) > 0:
#         account_information: AccountInformation = account_information[0]
#     else:
#         raise Exception(f"No account information found for account number: {account_number}")

#     return account_information