# World Watch API

World Watch advisories now can be retrieved using a dedicated REST API, located [here](https://api-ww.cert.orangecyberdefense.com).

A Swagger is available publicly for your development tests, with the corresponding JSON [here](https://api-ww.cert.orangecyberdefense.com/api/openapi.json)

If you need an account on this API, please contact us at worldwatch-request.ocd AT orange.com

## Permissions

### Keys

There are three types of keys:

*   EmailKeyAuthentication
    
*   LoginTokenAuthentication
    
*   APIKeyAuthentication
    

Different endpoints use different keys, and one user can have multiple keys at the same time.

You can know which endpoint uses which key by checking the [endpoints](#endpoints) section.

### User Role

There are four roles that a user can have:

*   Admin
    
*   Manager
    
*   User
    
*   Analyst
    

Different endpoints require different roles, and each user can have at most one role.

You can know which role is required for each endpoint by checking the [endpoints](#endpoints) section.

## User Management

In order to add a new user, you need:

*   Be a user with a role of **Manager** or **Admin**
    
*   Be authenticated with a **LoginTokenAuthentication**
    

You will need to:

1.  While authenticated, call the `/api/users [POST]` endpoint. It will return a user instance with an **id**
    
2.  While authenticated, call the `/api/users/{user_id}/send_invitation [POST]` endpoint. The user will receive an email with their **EmailKeyAuthentication**.
    
3.  The user should use his **EmailKeyAuthentication** and call the `/api/users/validate [POST]` endpoint with his password.
    
4.  If everything works correctly, the user should be able to login using the `/api/users/login [POST]` endpoint. This will return a **LoginTokenAuthentication**
    

In order to get an **APIKeyAuthentication**, you need to call the `/api/api_keys [POST]` endpoint while authenticated.

## API

### Request fields validation

Errors related to parsing requests fields, are returned in format:

```json
{
  "detail": [
    {
      "loc": [],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

- `loc` - shows the field when the error occured
- `msg` - is the error message
- `type` - is type of error

For example:

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "user_data",
        "email"
      ],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    },
    {
      "loc": [
        "body",
        "user_data",
        "first_name"
      ],
      "msg": "str type expected",
      "type": "type_error.str"
    },
    {
      "loc": [
        "body",
        "user_data",
        "last_name"
      ],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length",
      "ctx": {
        "limit_value": 1
      }
    }
  ]
}
```

### Errors

Errors that occurs when processing requests, creating models, authentication, checking permissions are returned in format: `{"detail": "error message"}`

### Dates

Date passed in requests will be treated as UTC except the cases when the timezone is passed in timestamp string.

### Permissions

If not met, returns error `You do not have permissions to perform this action.` with status code `403`

### Pagination

`Limit` and `Offset` can be set as query params for listing `users`, `content_block`, `advisories`, `threat_categories`, `sources`, `detection_rules`, `tags`, and `datalake_url`. Default limit is set in ENV `PAGINATION_PER_PAGE`.

## Endpoints

### Auth

#### Login

**URL:** `/api/auth/login`

**Permissions:** `Not set`

**Authorization:** `Not set`

**Throttling:** `ANON_REQUESTS_PER_MIN` /

**Description:**

Endpoint used to authenticate users email and password. In response user receive a key that is used to access other endpoints related to users and API keys.

User can be authenticated only if it exists in database and `is_active` flag is set to `True`.

After authentication user receive a `LoginToken` if it exists. If the token doesn’t exist, a new one is created with 8 hours expiration. If the token expires, it will be refreshed when user log in again.

If authentication fails, an error `Authentication failed, please verify if your account is active` will be returned with status code `401`.

### Users

#### **Get Users**

**URL:** `/api/users` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`

**Authorization:** `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get list of users. It returns only the users that are descendants of the requesting user.

#### **Create One**

**URL:** `/api/users` (`POST`)

**Permissions:** `MANAGER`, `ADMIN`

**Authorization:** `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to create new user with `manager` field set to the creating user.

When user is created by `MANAGER`, the values of `active_until`, `company` and `department` are set to values of the creating manager. Otherwise value of `active_until` is set to default value (365 days).

The email is validated by `EmailStr` type of [pydantic](https://docs.pydantic.dev/1.10/usage/types/) that where it use [python-email-validator](https://pypi.org/project/email-validator/) to validate value of email. The email must be unique, if any user with the same email already exists the error will be returned `User with email <email> already exists.`

User is created with role `USER`.

#### **Get Own Data**

**URL:** `/api/users/self` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get data of requesting user.

#### **Get One**

**URL:** `/api/users/{user_id}` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`

**Authorization:** `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get data of user for given id.

If the user is not found returns error `User not found for id: {user_id}.` with status code `404`.

If the user is not descendant of requesting user returns `You do not have permission to access user: {user_id}.` with status code `403`.

#### **Edit One**

**URL:** `/api/users/{user_id}` (`PATCH`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to update data of user for given id.

Fields that can be updated: `first_name`, `last_name`, `phone_number`, `manager`, `department`, `country`, `active_until`. All are optional.

Phone number should be passed in international format (starting with `+`).

If the user is not found returns error `User not found for id: {user_id}.` with status code `404`.

If the user is self or it’s not descendant of requesting user returns `You do not have permission to access user: {user_id}.` with status code `403`.

If requesting user is not `MANAGER` or `ADMIN` and tries to change `manager` field it returns error `User with role {role} cannot set manager.` with status code `403`.

If changing `manager` field but the manager is not found returns error `User not found for id: {manager_id}.` with status code `404`. If the manager is not descendant of requesting user returns `You do not have permission to access user: {manager_id}.` with status code `403`.

#### **Edit Role**

**URL:** `/api/users/{user_id}/role` (`PATCH`)

**Permissions:** `ADMIN`

**Authorization:** `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to update role of user for given id.

If changing role from `ADMIN` or `MANAGER` to a new one that is not one of them all of descendants of changed user will have `manager` field set to the requesting user.

If the user is not found returns error `User not found for id: {user_id}.` with status code `404`.

If changing role to `ADMIN` when the number of active admins is max returns error `Maximum number of admins has been reached.`

#### **Edit Company**

**URL:** `/api/users/{user_id}/company`(`PATCH`)

**Permissions:** `ADMIN`

**Authorization:** `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to update company of user for given id and all of his descendants.

If the user is not found returns error `User not found for id: {user_id}.` with status code `404`.

If the user is not descendant of requesting user returns `You do not have permission to access user: {user_id}.` with status code `403`.

#### **Edit Descendants**

**URL:** `/api/users/{user_id}/set_descendants`(`PATCH`)

**Permissions:** `ADMIN`

**Authorization:** `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to set manager of users for given ids.

Returns list of users ids with result messages in format `{id: message}`:

{
  "assignments": {
      {descendant\_id}: "Success",
      {not\_existing\_id}: "User not found for id: {not\_existing\_id}.",
      {not\_descendant\_id}: "You do not have permission to access user: {not\_descendant\_id}."
  }
}

If any user is not found message error is `User not found for id: {user_id}.`.

If any user is not descendant of requesting user returns `You do not have permission to access user: {user_id}.`.

#### **Edit Activation**

**URL:** `/api/users/{user_id}/set_activation`(`PATCH`)

**Permissions:** `ADMIN`

**Authorization:** `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to set `is_active` field to requested value of user for given id.

If the `is_active` is being set to `False` it also revokes all keys of that user. If the `is_active` is being set to `True` is also updates `active_until` field to same value of requesting user or to default value if the requested user is Admin.

If the `with_descendants` flag is `True` it also do the same changes for all of descendants. If the `with_descendants` flag is `False` `manager` of descendants is set to requesting user.

If the user is not found returns error `User not found for id: {user_id}.` with status code `404`.

If the user is not descendant of requesting user returns `You do not have permission to access user: {user_id}.` with status code `403`.

#### **Delete One**

**URL:** `/api/users/{user_id}` (`DELETE`)

**Permissions:** `ADMIN`, `MANAGER`

**Authorization:** `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to delete user for given id. Returns `204` status code if no errors occurs.

If the user is not found returns error `User not found for id: {user_id}.` with status code `404`.

If the user is not descendant of requesting user returns `You do not have permission to access user: {user_id}.` with status code `403`.

#### **Send Invitation**

**URL:** `/api/users/{user_id}/send_invitation` (`POST`)

**Permissions:** `ADMIN`, `MANAGER`

**Authorization:** `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to send invitation email to user for given id.

It creates `EmailKey` with 8h expiration and send it in the email body.

In the email user receive link to API Docs, where user can activate the account.

To activate Account authenticate in docs: {{ docs\_url }} using "EmailKeyAuthentication"
then use "Activate" endpoint.

Your authentication key is:
"EmailKeyAuthentication": "{{token\_key}}".

If the user is not found returns error `User not found for id: {user_id}.` with status code `404`.

If the user is not descendant of requesting user returns `You do not have permission to access user: {user_id}.` with status code `403`.

If the user is already verified returns error `User has been already verified` with status code `400`.

#### **Activate Account**

**URL:** `/api/users/activate`(`POST`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `EmailKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to verify user for given `EmailKey`. It set `verified` flag to `True` and set password to given value.

#### **Request Password Reset**

**URL:** `/api/users/{user_id}/send_password_reset-request` (`POST`)

**Permissions:** `Not set`

**Authorization:** `Not set`

**Throttling:** `ANON_REQUESTS_PER_MIN`

**Description:**

Endpoint used to send invitation email to user for given id. Returns `204` status code if no error occurs.

It creates `EmailKey` with 8h expiration and send it in the email body.

In the email user receive link to API Docs, where user can set new password.

To reset the password authenticate in docs: {{ docs\_url }} using "EmailKeyAuthentication"
then use "Reset Password" endpoint.

Your authentication key is:
"EmailKeyAuthentication": "{{token\_key}}".

Required data:
{
    "password": "<your new password>"
    "password\_confirmation": "<your new password>"
}

If the user is not found returns error `User not found for id: {user_id}.` with status code `404`.

#### **Reset Password**

**URL:** `/api/users/reset_password`(`POST`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `EmailKeyAuthentication` or `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to set password to given value. This will revoke all `EmailKeyAuthentication` and `LoginKeyAuthentication`.

### API Keys

#### **Get Own Keys**

**URL:** `/api/api_keys/`(`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `LoginKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get all API keys of requesting user.

#### **Create One**

**URL:** `/api/api_keys/`(`POST`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `LoginKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to create a new API key.

Expiration field is optional. If it’s nor passed the expiration date of that key on default is set to 1 year, if the user has lower expiration date it will be set to that value.

If number of existing tokens is already maxed it returns error `The limit of the keys is {api_key_max_number}.`.

If the value of passed expiration is lower than user expiration it returns error `Cannot set expiration date greater than user expiration.`.

#### **Get User Keys**

**URL:** `/api/api_keys/user/{user_id}`(`GET`)

**Permissions:** `MANAGER`, `ADMIN`

**Authorization:** `LoginKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get all API keys of user for given id.

If the user is not found returns error `User not found for id: {user_id}.` with status code `404`.

If the user is not descendant of requesting user returns `You do not have permission to access user: {user_id}.` with status code `403`.

#### **Update Expiration Date**

**URL:** `/api/api_keys/{token_id}`(`PATCH`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `LoginKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to update expiration date of key for given id.

If token is not found returns error `Not Found` with status code `404`.

If the token owner is not descendant of requesting user returns `You do not have permission to access user: {user_id}.` with status code `403`.

If the value of passed expiration is lower than user expiration it returns error `Cannot set expiration date greater than user expiration.`.

#### **Revoke Key**

**URL:** `/api/api_keys/{token_id}/revoke`(`PATCH`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `LoginKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to revoke key for given id.

If token is not found returns error `Not Found` with status code `404`.

If the token owner is not descendant of requesting user returns `You do not have permission to access user: {user_id}.` with status code `403`.

### Advisory

#### **List All**

**URL:** `/api/advisory` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get list of advisories.

List can be filtered by  `id`, `title`, `tdc_id`, `content`, `severity`, `tags_name`, `threat_category`, `created_before`, `created_after`, `updated_before`, `updated_after`. Searching by `tags_name` will return all **Advisories** that have these `tags` and all **Advisories** who have an associated **Content Block** that has these `tags`. Filters can be added to the request as query params. In addition, you can set the `sort_by` and `sort_order` query params to sort the results. By default, the results are sorted by `updated_at` in descending order. 

#### **Create One**

**URL:** `/api/advisory`(`POST`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to create new advisory for given data.

If given `threat_category` is not found the error will be raised: `ThreatCategory with title: {title} not found` with status code `404`

The `tags` will be set using existing records, if the records don't exists, new will be created.

#### **Get One**

**URL:** `/api/advisory/{advisory_id}` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get advisory data for given id.

If `advisory` is not found the error will be raised: `Advisory with id: {advisory_id} not found.` with status code `404`.

#### **Edit One**

**URL:** `/api/advisory/{advisory_id}`(`PATCH`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to update advisory for given data.

If `advisory` is not found the error will be raised: `Advisory with id: {advisory_id} not found.` with status code `404`.

If given `threat_category` is not found the error will be raised: `ThreatCategory with title: {title} not found` with status code `404`

The `tags` will be set using existing records, if the records don't exists, new will be created.

#### **Delete One**

**URL:** `/api/advisory/{advisory_id}` (`DELETE`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to delete advisory for given data. Returns `204` status code if no errors occurs.

If `advisory` is not found the error will be raised: `Advisory with id: {advisory_id} not found.` with status code `404`.

#### Get HTML

**URL:** `/api/advisory/{advisory_id}/html` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get an advisory as HTML.

If `advisory` is not found the error will be raised: `Advisory with id: {advisory_id} not found.` with status code `404`.

#### Get HTML Minimized

**URL:** `/api/advisory/{advisory_id}/html/minimized` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get an advisory as HTML. If there are mote then 6 updates, the HTML will display the latest 5 updates and the initial advisory. 

If advisory is not found the error will be raised: `Advisory with id: {advisory_id} not found`. with status code `404`.


### Content Block

#### **List All**

**URL:** `/api/content_block` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get list of content blocks.

List can be filtered by `id`, `title`, `advisory_id`, `threat_category`, `severity`, `content`, `created_before`, `created_after`, `updated_before`, `updated_after`,`tags_name`, `sources`, `detection_rules`, `datalake_url`. Filters can be added to the request as query params. In addition, you can set the `sort_by` and `sort_order` query params to sort the results. By default, the results are sorted by `updated_at` in descending order.

#### **Create One**

**URL:** `/api/content_block` (`POST`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to create new content block for given data.

The `analyst` and `last_modified_by` are set to user that creates content\_block.

If given `advisory` is not found the error will be raised: `Advisory with id: {advisory_id} not found.` with status code `404`

If given `threat_category` is not found the error will be raised: `ThreatCategory with title: {title} not found` with status code `404`

The `tags` will be set using existing records, if the records don't exists, new will be created.

If `sources`, `detection_rules` or `datalake_url` are not found the error will be raised: `No {name_of_field} found for given data.` with status code `404`

#### **List All Complete**

**URL:** `/api/content_block/complete` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get list of content blocks. The endpoint returns additional data `executive_summary`, `what_you_will_hear`, `what_it_means`, `what_you_should_do`.

List can be filtered by `id`, `title`, `advisory_id`, `threat_category`, `severity`, `content`, `created_before`, `created_after`, `updated_before`, `updated_after`,`tags_name`, `sources`, `detection_rules`, `datalake_url`. Filters can be added to the request as query params. In addition, you can set the `sort_by` and `sort_order` query params to sort the results. By default, the results are sorted by `updated_at` in descending order.

#### **Get One**

**URL:** `/api/content_block/{content_block_id}` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get a content block data for given id.

If the content block is not found returns error `Content block with id: {content_block_id} not found.` with status code `404`.

#### **Edit One**

**URL:** `/api/content_block/{content_block_id}` (`PATCH`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to update a content block for given data.

If the content\_block is not found returns error `Content block with id: {content_block_id} not found.` with status code `404`.

The `last_modified_by` is set to user that updates content block.

If given `advisory` is not found the error will be raised: `Advisory with id: {advisory_id} not found.` with status code `404`

If given `threat_category` is not found the error will be raised: `ThreatCategory with title: {title} not found` with status code `404`

The `tags` will be set using existing records, if the records don't exists, new will be created.

If `sources`, `detection_rules` or `datalake_url` are not found the error will be raised: `No {name_of_field} found for given data.` with status code `404`

#### **Delete One**

**URL:** `/api/content_block/{content_block_id}` (`DELETE`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to delete a content block for given id. Returns `204` status code if no errors occurs.

If the content\_block is not found returns error `Content block with id: {content_block_id} not found.` with status code `404`.

#### **Get One Minimized**

**URL:** `/api/content_block/{content_block_id}/minimized` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get a content block data for given id. The endpoint does not return the content, only the metadata of the block.

If the content block is not found returns error `Content block with id: {content_block_id} not found.` with status code `404`.

#### **Get HTML**

**URL:** `/api/content_block/{content_block_id}/html` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get a content block as HTML.

If `content_block` is not found the error will be raised: `Content block with id: {content_block_id} not found.` with status code `404`.

### Detection Rule

#### **List All**

**URL:** `/api/detection_rule`(`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get list of detection rules.

#### **Create One**

**URL:** `/api/detection_rule`(`POST`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to create new detection rule for given data.

If given `content_block` is not found the error will be raised: `Content block with id: {content_block_id} not found` with status code `404`.

#### **Get One**

**URL:** `/api/detection_rule/{detection_rule_id}` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get detection\_rule data for given id.

If `detection_rule` is not found the error will be raised: `DetectionRule with id: {detection_rule_id} not found.` with status code `404`.

#### **Edit One**

**URL:** `/api/detection_rule/{detection_rule_id}`(`PATCH`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to update detection\_rule for given data.

If `detection_rule` is not found the error will be raised: `DetectionRule with id: {source_id} not found.` with status code `404`.

If given content\_block is `None` the current content\_block will be unlinked.

If given `content_block` is not found the error will be raised: `Content block with id: {content_block_id} not found` with status code `404`

#### **Delete One**

**URL:** `/api/detection_rule/{detection_rule_id}`(`DELETE`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to delete a detection rule for given `id`. Returns `204` status code if no errors occurs.

If `detection_rule` is not found the error will be raised: `DetectionRule with id: {source_id} not found.` with status code `404`.

### Source

#### **List All**

**URL:** `/api/source` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get list of sources.

#### **Create One**

**URL:** `/api/source`(`POST`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to create new source for given data.

If given `content_block` is not found the error will be raised: `Content block with id: {content_block_id} not found` with status code `404`

#### **Get One**

**URL:** `/api/source/{source_id}` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get source data for given id.

If `source`not found the error will be raised: `Source with id {source_id} not found.` with status code `404`.

#### Edit One

**URL:** `/api/source/{source_id}`(`PATCH`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to update source for given data.

If `source` is not found the error will be raised: `Source with id {source_id} not found.` with status code `404`.

If given `content_block` is not found the error will be raised: `Content block with id: {content_block_id} not found` with status code `404`

#### **Delete One**

**URL:** `/api/source/{source_id}`(`DELETE`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to delete a source for given `id`. Returns `204` status code if no errors occurs.

If `source` is not found the error will be raised: `Source with id {source_id} not found.` with status code `404`.

### Datalake Url

#### **List All**

**URL:** `/api/datalake_url` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get list of datalake urls.

#### **Create One**

**URL:** `/api/datalake_url`(`POST`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to create new datalake url for given data.

If given `content_block` is not found the error will be raised: `Content block with id: {content_block_id} not found` with status code `404`

#### **Get One**

**URL:** `/api/source/{datalake_url_id}` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get datalake url data for given id.

If `datalake_url` not found the error will be raised: `DatalakeUrl with id: {datalake_url_id} not found.` with status code `404`.

#### Edit One

**URL:** `/api/source/{datalake_url_id}`(`PATCH`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to update a datalake url for given data.

If `datalake_url` is not found the error will be raised: `DatalakeUrl with id: {datalake_url_id} not found.` with status code `404`.

If given `content_block` is not found the error will be raised: `Content block with id: {content_block_id} not found` with status code `404`

#### **Delete One**

**URL:** `/api/source/{datalake_url_id}`(`DELETE`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to delete a datalake url for given id. Returns `204` status code if no errors occurs.

If `datalake_url` is not found the error will be raised: `DatalakeUrl with id: {datalake_url_id} not found.` with status code `404`.

### Tags

#### **List All**

**URL:** `/api/tags`(`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get list of tags.

#### **Create One**

**URL:** `/api/tags`(`POST`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to create new tag for given data.

Tag name is unique. When creating tag with existing name the error will be raised: `Tag with name {name} already exists.`

#### **Get One**

**URL:** `/api/tags/{tag_name}` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get tag data for given name.

If `tag` is not found the error will be raised: `Tag with name {tag_name} not found.` with status code `404`.

#### **Delete One**

**URL:** `/api/tags/{tag_name}`(`DELETE`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to delete tag for given data. Returns `204` status code if no errors occurs.

If `tag` is not found the error will be raised: `Tag with name {tag_name} not found.` with status code `404`.

### Threat Category

#### **List All**

**URL:** `/api/threat_category` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get list of threat categories.

#### **Create One**

**URL:** `/api/threat_category`(`POST`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to create new threat category for given data.

Threat category title is unique. When trying to create a record with existing title the error will be raised: `ThreatCategory with title {title} already exists.` with status code `400`

#### **Get One**

**URL:** `/api/threat_category /{threat_category_title}` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get threat category data for given title.

If `threat_category`is not found the error will be raised: `ThreatCategory with title: {threat_category_title} not found.` with status code `404`.

#### **Delete One**

**URL:** `/api/threat_category/{threat_category_title}`(`DELETE`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to delete a threat category for given title. Returns `204` status code if no errors occurs.

If `threat_category`is not found the error will be raised: `ThreatCategory with title: {threat_category_title} not found.` with status code `404`.


## Models

### Users

#### Table: `Users`

| Column | Type | Constraints |
| --- | --- | --- |
| id  | integer |     |
| email | string | unique, max\_length=100, required |
| username | string | auto\_add (set to email value when creating record) |
| password | string | hashed, required |
| first\_name | string | max\_length=50, required |
| last\_name | string | max\_length=50, required |
| last\_login | datetime | auto\_add |
| is\_active | boolean | True/False, not active can’t login |
| date\_joined | datetime | auto\_add |
| phone\_number | string | max\_length=16, optional |
| company | string | max\_length=100, optional |
| department | string | max\_length=50, optional |
| country | string | max\_length=50, optional |
| verified | boolean | default is False |
| active\_until | datetime | optional |
| role | string | choices=\[admin, manager, user, analyst\], default=user |

#### Table: `Tokens`

| Column | Type | Constraints |
| --- | --- | --- |
| id  | integer |     |
| name | string | max\_length=64, optional |
| user\_id | integer | not null |
| key | string | max\_length=64, unique, auto-generated |
| expiration | datetime | default=default\_login\_key\_expiration |
| type | string | choices=\[auth, api\_key, email\_key\] |
| revoked | boolean | default is False |

### Content

#### Table: `Threat Categories`

| Column | Type | Constraints |
| --- | --- | --- |
| id  | integer |     |
| title | string | max\_length=50, unique |

- - -

#### Table: `Tags`

| Column | Type | Constraints |
| --- | --- | --- |
| id  | integer |     |
| name | string | max\_length=100, unique |

- - -

#### Table: `Advisories`

| Column | Type | Constraints |
| --- | --- | --- |
| id  | integer |     |
| tdc\_id | integer | null=True, blank=True |
| title | string | max\_length=200 |
| severity | integer | allowed\_range \[0, 5\] |
| threat\_category | integer |     |
| timestamp\_created | datetime |     |
| timestamp\_updated | datetime |     |
| license\_agreement | string | max\_length=2048, default="This advisory has been prepared and is the property of Orange Cyberdefense. Please don't redistribute this content without our agreement." |

- - -

#### Table: `Content Blocks`

| Column | Type | Constraints |
| --- | --- | --- |
| id  | integer |     |
| advisory | integer | not null |
| index | integer | default=0, null=False, minimum=0 |
| title | string | max\_length=200 |
| severity | integer | allowed\_range \[0, 5\] |
| analyst | integer | null=True |
| last\_modified\_by | integer | null=True |
| executive\_summary | text |     |
| what\_you\_will\_hear | text |     |
| what\_it\_means | text |     |
| what\_you\_should\_do | text |     |
| what\_we\_are\_doing | text |     |
| other | text |     |
| threat\_category | integer |     |
| timestamp\_created | datetime |     |
| timestamp\_updated | datetime |     |

- - -

#### Table: `Sources`

| Column | Type | Constraints |
| --- | --- | --- |
| id  | integer |     |
| content\_block | integer | not null |
| title | string | default=”” |
| description | text | blank=true |
| url | string | max\_length=500 |
| type | string | \[external, internal\] |

- - -

#### Table: `Detection Rules`

| Column | Type | Constraints |
| --- | --- | --- |
| id  | integer |     |
| content\_block | integer | not null |
| title | string | default=”” |
| description | text | blank=true |
| content | text |     |

- - -

#### Table: `Datalake Url`

| Column | Type | Constraints |
| --- | --- | --- |
| id  | integer |     |
| content\_block | integer | not null |
| title | string | default=”” |
| description | text | blank=true |
| url | string | max\_length=500 |

