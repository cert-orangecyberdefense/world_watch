# Changelog

All notable changes to this project will be documented in this file.

## Production - v1.8
> 20-10-2025

### Improvements:
1. Added search fields on `datalake_url`, `detection_rule`, `source`, and `tags`

### Features:
1. Added an **RSS feeds** ([info](https://github.com/cert-orangecyberdefense/world_watch/blob/main/RSS.md))
    - **Free feed** with limited content
    - **Premium feeds** accessible to users with Manager role

## Production - v1.7
> 11-06-2025

### Production - v1.7.4
> 11-09-2025

#### Changes:
1. Removal of `threat_category`

### Improvements:
1. **Cleanup of query parameters** types in GET requests
 
### Changes:
1. Removal of `tags_name` search parameter
2. Indicate the **(future) deprecation** of `threat_category`

### Features:
- Addition of `categories` field for each **Content Block**:
    - Filter in GET `/api/advisories` & `/api/content_block` & `/api/content_block/complete`
    - Include in GET `/*/html` & `/*/html/minimized`
    - Response field for every **Content Block**
    - Response field for every **Advisory**: a **concatenation** of the `categories` of all its **Content Blocks**

## Production - v1.6
> 02-01-2025

### Production - v1.6.3
> 17-04-2025

#### Changes

1. Email routes now require **email** instead of **user_id**. The routes were changed to reflect this change:
    - POST `/api/users/{user_id}/send_password_reset` → POST `/api/users/send_password_reset`
    - POST `/api/users/{user_id}/send_invitation` → POST `/api/users/send_invitation`
	
2. Addition of **change password** route to be able to modify password while connected
	- POST `/api/users/change_password`
	
3. **Email** and **Login** tokens will be revoked after doing sensitive operations:
	- POST `/api/users/activate`
    - POST `/api/users/change_password` 
    - POST `/api/users/reset_password` 

### Production - v1.6.2
> 25-03-2025

#### Improvements

1. Added small description for **tags**, **tags_name**, and **severity** fields in GET `/api/advisory` & `/api/content_block/` & `/api/content_block/complete/` 

#### Bugfix

1. Fix bug where filtering using **tags** or **tags_name** will return incomplete results in GET `/api/advisory` & `/api/content_block/` & `/api/content_block/complete/` 

### Production - v1.6.1
> 09-01-2025

#### Improvements

1. Support for filtering **advisories** and **content_blocks** by multiple **tags**:
    - Renaming of filter field **tags_name** to **tags** in GET `/api/advisory` & `/api/content_block/` & `/api/content_block/complete/` 
    - Field now supports multiple values separated by commas
2. Sorted response of GET `/api/tags` & `/api/threat_categories` alphabetically

### Improvements

1. More detailed logging of the API
2. Normalize all tags to lowercase
3. Remove incorrect ISO in tag `victim:country=uk` and replace with `victim:country=gb`
4. Add additional fields in output of some requests:
    - GET `/api/detection_rule/{id}` & `/api/source/{id}` & `/api/datalake_url/{id}`: add **advisory** and **content_block** fields in response
    -  GET `/api/tags/{tag_name}` & `/api/threat_categories/{threat_category_title}`: add **advisories** and **content_blocks** fields in response
    - POST/PATCH `/api/detection_rule/` & `/api/source/` & `/api/datalake_url/`: add **advisory** field in response

## Production - v1.5
> 05-08-2024

### Production - v1.5.4
> 28-10-2024

#### Improvements

- GET `/*/html` & `/*/html/minimized`: 
    - better formatting for **tags** 
    - removed redundant `<p>` tags in the different content sections
    - sorted **tags**, **regions**, and **sectors** alphabetically

#### Bugfix

- fixed typo in the HTML generation that caused *Internal Server Error* when a **detection rule** had a description

#### Other

- redirection to `/api/docs` instead of **404**

### Production - v1.5.2
> 14-08-2024

#### Features

1. GET/POST/PATCH `/api/content_block` & `/api/content_block/complete` & `/api/content_block/{id}` & `/api/content_block/{id}/minimized`:
    - Add **advisory_tags** field in response 

### Features

1. GET `/api/advisory` & `/api/content_block` & `/api/content_block/complete`:
    - support search using the **id** field 

### Improvements

1. GET `/*/html` & `/*/html/minimized`:
    - better formatting for **tags**
    - colored titles
    - better font size and family
    - justified text
    - removed section numbers
    - include only sections with content
    - other minor improvements

### Bugfix

- force **tags** to be lowercase
- fix invalid **datalake_url** in HTML generation


## Production - v1.4
> 27-06-2024

### Features

1. GET `/api/advisory` & `/api/content_block` & `/api/content_block/complete`:
    - support search multiple values for **severity** and **threat_category** (comma separated) -> **Type of Severity in request parameters has been changed from `int` to `string`**
    i.e.
    - severity=1 -> 266 results
    vs.
    - severity=1,2,3 -> 779 results

2. GET `/api/content_block/complete`:
    - add new **sort_by** filter, with 7 parameters: *id, severity, timestamp*, etc.
    - add new **sort_order** filter: *asc/desc*

3. PATCH `/api/advisory/{advisory_id}` & `/api/content_block/{content_block_id}`:
    - does not update **timestamp_updated** if only **tags** are updated

### Bugfix
- make sorting by **title** and **threat_category** case insensitive


## Production - v1.3
> 20-06-2024
    
### Features

1. GET `/api/advisory`:
    - new parameter to search by **tdc_id** 
    - parameter to search by tags: respond if **advisories** OR **content_block** is tagged (NB: advisories are often tagged with a single tag, but each **content_block** has possibly multiple ones. Details of an advisories using `/advisories/ID` will give you which **content_block** has the searched for tag if needed)

2. GET `api/advisories` & `api/content_block`:
    - add *HH-MM* or *HH-MM-SS* to search by **created/updated timestamps** ($date-time), instead of only $date
        i.e.
        - created_after=2024-04-16 -> 15 results
        vs. 
        - created_after=2024-04-16 15:12 -> 14 results
        vs. 
        - created_after=2024-04-16 15:12:07 -> 13 results
    - add new **sort_by** filter, with 7 parameters: *id, severity, timestamp*, etc.
    - add new **sort_order** filter: *asc/desc*

3. POST `api/users/reset_password`:
    - can be used with *Login/EmailToken*, thus can be used directly without `api/users/send_password_reset_request` first
    - revokes existing *Email/LoginToken* directly, in case of compromise for example

4. new HTML endpoint `/api/advisory/{​​​​​​​advisory_id}​​​​​​​/html/minimized`
    - new endpoint for smaller export in HTML that outputs the information of AT MOST the last 5 **content_blocks** + **initial block**


### Bugfix

- search by **threat_category_title** not working
- Add **UserID** in activation email