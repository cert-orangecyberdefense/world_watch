# Changelog

All notable changes to this project will be documented in this file.

## Production - v1.6
> 02-01-2025

### Improvements

1. More detailed logging of the API
2. Normalize all tags to lowercase
3. Remove incorrect ISO in tag `victim:country=uk` and replace with `victim:country=gb`
4. Add additional fields in output of some requests:
    - GET `/api/detection_rule/{id}` & `/api/source/{id}` & `/api/datalake_url/{id}`: add **advisory** and **content_block** fields in response
    -  GET `/api/tags/{tag_name}` & `/api/threat_categories/{threat_category_title}`: add **advisories** and **content_blocks** fields in response
    - POST/PATCH `/api/detection_rule/` & `/api/source/` & `/api/datalake_url/`: add **advisory** field in response

### Production - v1.6.1
> 09-01-2025

### Improvements

1. Support for filtering **advisories** and **content_blocks** by multiple **tags**:
    - Renaming of filter field **tags_name** to **tags** in GET `/api/advisory` & `/api/content_block/` & `/api/content_block/complete/` 
    - Field now supports multiple values separated by commas
2. Sorted response of GET `/api/tags` & `/api/threat_categories` alphabetically

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