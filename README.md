# World Watch API

World Watch advisories now can be retrieved using a dedicated REST API, located [here](https://api-ww.cert.orangecyberdefense.com).

A Swagger is available publicly for your development tests, with the corresponding JSON [here](https://api-ww.cert.orangecyberdefense.com/api/openapi.json)

If you need an account on this API, please contact us at worldwatch-request.ocd AT orange.com

Each **Advisory** acts as a container for related information. It doesn’t hold all
the raw details itself—instead, it is composed of one or more **Updates**(`Content Blocks`),
which are the actual units of data.

Each **Update**(`Content Block`) contains the actual data, the **Advisory** acts as an umbrella and brings these blocks together under a common theme or context.


## Permissions

### Keys

There are three types of keys:
- EmailKeyAuthentication
- LoginTokenAuthentication
- APIKeyAuthentication
    

Different endpoints use different keys, and one user can have multiple keys at the same time.

You can know which endpoint uses which key by checking the [endpoints](#endpoints) section.

### User Role

There are four roles that a user can have:
- Admin
- Manager
- User
- Analyst
    

Different endpoints require different roles, and each user can have at most one role.

You can know which role is required for each endpoint by checking the [endpoints](#endpoints) section.

## User Management

In order to add a new user, you need:

*   Be a user with a role of **Manager** or **Admin**
    
*   Be authenticated with a **LoginTokenAuthentication**
    

You will need to:

1.  While authenticated, call the `/api/users [POST]` endpoint. It will return a user instance with an **id**
    
2.  While authenticated, call the `/api/users/send_invitation [POST]` endpoint. The user will receive an email with their **EmailKeyAuthentication**.
    
3.  The user should use his **EmailKeyAuthentication** and call the `/api/users/validate [POST]` endpoint with his password.
    
4.  If everything works correctly, the user should be able to login using the `/api/users/login [POST]` endpoint. This will return a **LoginTokenAuthentication**
    

In order to get an **APIKeyAuthentication**, you need to call the `/api/api_keys [POST]` endpoint while authenticated.

## RSS

An **RSS** is provided to facilitate the integration of our advisories with any RSS reader.

Free RSS feeds provide limited content, while **premium RSS feeds offer full access** and allow filtering by tags.

A complete explanation of how to use the **RSS** is provided [here](./RSS.md)

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

`Limit` and `Offset` can be set as query params for listing `users`, `content_block`, `advisories`, `categories`, `sources`, `detection_rules`, `tags`, and `datalake_url`. Default limit is set in ENV `PAGINATION_PER_PAGE`.

## Endpoints

### Auth

#### Login

**URL:** `/api/auth/login`

**Permissions:** `Not set`

**Authorization:** `Not set`

**Throttling:** `ANON_REQUESTS_PER_MIN` /

**Description:**

User can be authenticated only if it exists in database and `is_active` flag is set to `True`.

After authentication user receive a `LoginToken` if it exists. If the token doesn’t exist, a new one is created with 8 hours expiration. If the token expires, it will be refreshed when user log in again.

If authentication fails, an error `Authentication failed, please verify if your account is active` will be returned with status code `401`.

### Users

#### Get Users

**URL:** `/api/users` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`

**Authorization:** `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get list of users. It returns only the users that are descendants of the requesting user.

#### Create One

**URL:** `/api/users` (`POST`)

**Permissions:** `MANAGER`, `ADMIN`

**Authorization:** `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to create new user with `manager` field set to the creating user.

When user is created by `MANAGER`, the values of `active_until`, `company` and `department` are set to values of the creating manager. Otherwise value of `active_until` is set to default value (365 days).

The email is validated by `EmailStr` type of [pydantic](https://docs.pydantic.dev/1.10/usage/types/) that where it use [python-email-validator](https://pypi.org/project/email-validator/) to validate value of email. The email must be unique, if any user with the same email already exists the error will be returned `User with email <email> already exists.`

User is created with role `USER`.

#### Get Own Data

**URL:** `/api/users/self` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get data of requesting user.

#### Get One

**URL:** `/api/users/{user_id}` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`

**Authorization:** `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get data of user for given id.

If the user is not found returns error `User not found for id: {user_id}.` with status code `404`.

If the user is not descendant of requesting user returns `You do not have permission to access user: {user_id}.` with status code `403`.

#### Edit One

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

#### Delete One

**URL:** `/api/users/{user_id}` (`DELETE`)

**Permissions:** `ADMIN`, `MANAGER`

**Authorization:** `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to delete user for given id. Returns `204` status code if no errors occurs.

If the user is not found returns error `User not found for id: {user_id}.` with status code `404`.

If the user is not descendant of requesting user returns `You do not have permission to access user: {user_id}.` with status code `403`.

#### Send Invitation

**URL:** `/api/users/send_invitation` (`POST`)

**Permissions:** `ADMIN`, `MANAGER`

**Authorization:** `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to send invitation email to user for given email.

It creates `EmailKey` with 8h expiration and send it in the email body.

In the email user receive link to API Docs, where user can activate the account.

If the user is already verified returns error `User has been already verified` with status code `400`.

#### Activate Account

**URL:** `/api/users/activate`(`POST`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `EmailKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to verify user for given `EmailKey`. It set `verified` flag to `True` and set password to given value.

#### Reset Password

**URL:** `/api/users/change_password`(`POST`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to modify the password to given value for a user that is already logged in. This will revoke all `EmailKeyAuthentication` and `LoginKeyAuthentication`.


#### Request Password Reset

**URL:** `/api/users/send_password_reset_request` (`POST`)

**Permissions:** `Not set`

**Authorization:** `Not set`

**Throttling:** `ANON_REQUESTS_PER_MIN`

**Description:**

Endpoint used to send the password reset email to the user for given email. Returns `202` status code if no error occurs.

It creates `EmailKey` with 8h expiration and send it in the email body.

In the email user receive link to API Docs, where user can set new password.

#### Reset Password

**URL:** `/api/users/reset_password`(`POST`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `EmailKeyAuthentication` or `LoginTokenAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to set password to given value. This will revoke all `EmailKeyAuthentication` and `LoginKeyAuthentication`.

### API Keys

#### Get Own Keys

**URL:** `/api/api_keys/`(`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `LoginKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get all API keys of requesting user.

#### Create One

**URL:** `/api/api_keys/`(`POST`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `LoginKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to create a new API key.

Expiration field is optional. If it’s nor passed the expiration date of that key on default is set to 1 year, if the user has lower expiration date it will be set to that value.

If number of existing tokens is already maxed it returns error `The limit of the keys is {api_key_max_number}.`.

If the value of passed expiration is lower than user expiration it returns error `Cannot set expiration date greater than user expiration.`.

#### Get User Keys

**URL:** `/api/api_keys/user/{user_id}`(`GET`)

**Permissions:** `MANAGER`, `ADMIN`

**Authorization:** `LoginKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get all API keys of user for given id.

If the user is not found returns error `User not found for id: {user_id}.` with status code `404`.

If the user is not descendant of requesting user returns `You do not have permission to access user: {user_id}.` with status code `403`.

#### Update Expiration Date

**URL:** `/api/api_keys/{token_id}`(`PATCH`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `LoginKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to update expiration date of key for given id.

If token is not found returns error `Not Found` with status code `404`.

If the token owner is not descendant of requesting user returns `You do not have permission to access user: {user_id}.` with status code `403`.

If the value of passed expiration is lower than user expiration it returns error `Cannot set expiration date greater than user expiration.`.

#### Revoke Key

**URL:** `/api/api_keys/{token_id}/revoke`(`PATCH`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `LoginKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to revoke key for given id.

If token is not found returns error `Not Found` with status code `404`.

If the token owner is not descendant of requesting user returns `You do not have permission to access user: {user_id}.` with status code `403`.

### Advisory

#### List All

**URL:** `/api/advisory` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get list of advisories.

The `categories` field in the response corresponds to a **concatenation** of all the `categories` of this advisory's content blocks.

List can be filtered by  `id`, `title`, `tdc_id`, `content`, `severity`, `tags`, `categories`, `sources`, `datalake_urls`, `created_before`, `created_after`, `updated_before`, `updated_after`. You can pass multiple values separated by commas to `tags` and `categories`. Searching by `tags` will return all **Advisories** that have these `tags` and all **Advisories** who have an associated **Content Block** that has these `tags`. Searching by `categories` will return all **Advisories** that have at least one **Content Block** that has these `categories`. Filters can be added to the request as query params. In addition, you can set the `sort_by` and `sort_order` query params to sort the results. By default, the results are sorted by `updated_at` in descending order. 

#### Get One

**URL:** `/api/advisory/{advisory_id}` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get advisory data for given id.

The `categories` field in the response corresponds to a **concatenation** of all the `categories` of this advisory's content blocks.

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

Endpoint used to get an advisory as HTML. If there are more than 4 updates, the HTML will display the latest 3 updates and the initial advisory. 

If advisory is not found the error will be raised: `Advisory with id: {advisory_id} not found`. with status code `404`.

#### Get Markdown

**URL:** `/api/advisory/{advisory_id}/markdown` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get an advisory as Markdown.

If `advisory` is not found the error will be raised: `Advisory with id: {advisory_id} not found.` with status code `404`.

#### Get Markdown Minimized

**URL:** `/api/advisory/{advisory_id}/markdown/minimized` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get an advisory as Markdown. If there are more than 4 updates, the Markdown will display the latest 3 updates and the initial advisory. 

If advisory is not found the error will be raised: `Advisory with id: {advisory_id} not found`. with status code `404`.


### Content Block

#### List All

**URL:** `/api/content_block` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get list of content blocks.

The `advisory_tags` field in the response corresponds to the **tags of the parent advisory**.

List can be filtered by `id`, `title`, `advisory_id`, `categories`, `severity`, `content`, `created_before`, `created_after`, `updated_before`, `updated_after`,`tags`, `sources`, `detection_rules`, `datalake_urls`. You can pass multiple values separated by commas to `tags` and `categories`. Filters can be added to the request as query params. In addition, you can set the `sort_by` and `sort_order` query params to sort the results. By default, the results are sorted by `updated_at` in descending order.


#### List All Complete

**URL:** `/api/content_block/complete` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get list of content blocks. The endpoint returns additional data `executive_summary`, `what_you_will_hear`, `what_it_means`, `what_you_should_do`.

List can be filtered by `id`, `title`, `advisory_id`, `categories`, `severity`, `content`, `created_before`, `created_after`, `updated_before`, `updated_after`,`tags`, `sources`, `detection_rules`, `datalake_urls`. You can pass multiple values separated by commas to `tags` and `categories`. Filters can be added to the request as query params. In addition, you can set the `sort_by` and `sort_order` query params to sort the results. By default, the results are sorted by `updated_at` in descending order.

#### Get One Minimized

**URL:** `/api/content_block/{content_block_id}/minimized` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get a content block data for given id. The endpoint does not return the content, only the metadata of the block.

If the content block is not found returns error `Content block with id: {content_block_id} not found.` with status code `404`.

#### Get HTML

**URL:** `/api/content_block/{content_block_id}/html` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get a content block as HTML.

If `content_block` is not found the error will be raised: `Content block with id: {content_block_id} not found.` with status code `404`.

#### Get Markdown

**URL:** `/api/content_block/{content_block_id}/markdown` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get a content block as Markdown.

If `content_block` is not found the error will be raised: `Content block with id: {content_block_id} not found.` with status code `404`.

### Detection Rule

#### List All

**URL:** `/api/detection_rule`(`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get list of detection rules.

#### Create One

**URL:** `/api/detection_rule`(`POST`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to create new detection rule for given data.

If given `content_block` is not found the error will be raised: `Content block with id: {content_block_id} not found` with status code `404`.

#### Get One

**URL:** `/api/detection_rule/{detection_rule_id}` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get detection\_rule data for given id.

If `detection_rule` is not found the error will be raised: `DetectionRule with id: {detection_rule_id} not found.` with status code `404`.

#### Edit One

**URL:** `/api/detection_rule/{detection_rule_id}`(`PATCH`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to update detection\_rule for given data.

If `detection_rule` is not found the error will be raised: `DetectionRule with id: {source_id} not found.` with status code `404`.

If given content\_block is `None` the current content\_block will be unlinked.

If given `content_block` is not found the error will be raised: `Content block with id: {content_block_id} not found` with status code `404`

#### Delete One

**URL:** `/api/detection_rule/{detection_rule_id}`(`DELETE`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to delete a detection rule for given `id`. Returns `204` status code if no errors occurs.

If `detection_rule` is not found the error will be raised: `DetectionRule with id: {source_id} not found.` with status code `404`.

### Source

#### List All

**URL:** `/api/source` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get list of sources.

#### Create One

**URL:** `/api/source`(`POST`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to create new source for given data.

If given `content_block` is not found the error will be raised: `Content block with id: {content_block_id} not found` with status code `404`

#### Get One

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

#### Delete One

**URL:** `/api/source/{source_id}`(`DELETE`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to delete a source for given `id`. Returns `204` status code if no errors occurs.

If `source` is not found the error will be raised: `Source with id {source_id} not found.` with status code `404`.

### Datalake Url

#### List All

**URL:** `/api/datalake_url` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get list of datalake urls.

#### Create One

**URL:** `/api/datalake_url`(`POST`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to create new datalake url for given data.

If given `content_block` is not found the error will be raised: `Content block with id: {content_block_id} not found` with status code `404`

#### Get One

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

#### Delete One

**URL:** `/api/source/{datalake_url_id}`(`DELETE`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to delete a datalake url for given id. Returns `204` status code if no errors occurs.

If `datalake_url` is not found the error will be raised: `DatalakeUrl with id: {datalake_url_id} not found.` with status code `404`.

### Tags

#### List All

**URL:** `/api/tags`(`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get list of tags.

#### Create One

**URL:** `/api/tags`(`POST`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to create new tag for given data.

Tag name is unique. When creating tag with existing name the error will be raised: `Tag with name {name} already exists.`

#### Get One

**URL:** `/api/tags/{tag_name}` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get tag data for given name.

If `tag` is not found the error will be raised: `Tag with name {tag_name} not found.` with status code `404`.

#### Delete One

**URL:** `/api/tags/{tag_name}`(`DELETE`)

**Permissions:** `ANALYST`, `ADMIN`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to delete tag for given data. Returns `204` status code if no errors occurs.

If `tag` is not found the error will be raised: `Tag with name {tag_name} not found.` with status code `404`.

### Categories

#### List All

**URL:** `/api/categories/` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get list of categories.

#### Get One

**URL:** `/api/categories/{category_name}` (`GET`)

**Permissions:** `MANAGER`, `ADMIN`, `ANALYST`, `USER`

**Authorization:** `APIKeyAuthentication`

**Throttling:** `USER_REQUESTS_PER_MIN`

**Description:**

Endpoint used to get category data for given category name.

If `category`is not found the error will be raised: `Category with title: {category_name} not found.` with status code `404`.

