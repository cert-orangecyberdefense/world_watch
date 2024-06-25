# Changelog

All notable changes to this project will be documented in this file.

## Production - v1.4
> 27-06-2024

### Features

1. GET `/api/advisories` & `/api/content_block` & `/api/content_block/complete`:
    - support search multiple values for **severity** and **threat_category** (comma separated) -> **Type of Severity in request parameters has been changed from `int` to `string`**
    i.e.
    - severity=1 -> 266 results
    vs.
    - severity=1,2,3 -> 779 results

2. GET `/api/content_block/complete`:
    - add new **sort_by** filter, with 7 parameters: *id, severity, timestamp*, etc.
    - add new **sort_order** filter: *asc/desc*

3. PATCH `/api/advisories/{advisory_id}` & `/api/content_block/{content_block_id}`:
    - does not update **timestamp_updated** if only **tags** are updated

### Bugfix
- make sorting by **title** and **threat_category** case insensitive


## Production - v1.3
> 20-06-2024
    
### Features

1. GET `/api/advisories`:
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