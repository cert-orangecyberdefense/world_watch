# World Watch RSS

**World Watch** provides two types of RSS feeds: **Free** and **Premium**. These feeds allow you to stay up to date with the latest cyber threats via our advisories, by easily integrating them in your in-house tools and workflows.

---

## RSS Types

| Type    | Content             | Summary   | HTML Full Advisory | Filtering |
| ------- | ------------------- | --------- | ------------------ | --------- |
| Free    | Limited (1/5 items) | Truncated | ❌                  | ❌         |
| Premium | Full                | Complete  | ✅                  | ✅         |


**Free RSS**

* **Limited content**: Only a subset of advisories is included.
* **Item sampling**: At most 1 out of every 5 items is shown.
* **Truncated summaries**: Only part of the executive summary is available.
* Ideal for general monitoring without full access.

**Premium RSS**

* **Full content**: All advisories and updates are included.
* **Complete summaries**: No truncation of executive summaries.
* **HTML encoded content**: Full advisory content available in HTML format.
* **Filtering support**: Filter by sectors, regions, countries, categories, and tags.

---

## Available Endpoints

| Endpoint                                                                            | Description                               |
| ------------------------------------------------------------------------------------| ----------------------------------------- |
| `https://api-ww.cert.orangecyberdefense.com/rss`                                    | Free advisories feed. No key required     |
| `https://api-ww.cert.orangecyberdefense.com/rss/advisories/{RSS_API_KEY}?<filters>` | Premium advisories with optional filters. |
| `https://api-ww.cert.orangecyberdefense.com/rss/updates/{RSS_API_KEY}?<filters>`    | Premium updates with optional filters.    |

Notes:
- Replace `{RSS_API_KEY}` with an **rss_key** you generate (see [Premium Access](#premium-access)).
- Optional filters are added as a query string (see [Filtering](#filtering)).
- All endpoints return RSS 2.0 XML.

---

## Premium Access

To access premium RSS feeds:

**Create an RSS API Key**

* Use the [`/api/api_keys`](https://api-ww.cert.orangecyberdefense.com/api/docs#/API%20Keys/create_key) **POST** endpoint to generate a key of type `rss_key`.
* Only users with **Manager** role can create RSS API keys.

    ```js
    POST /api/api_keys
    Content-Type: application/json
    Authorization: <your-auth-token>

    {
        "type": "rss_key",
        "expiration": "YYYY-MM-DD",
        "name": "World Watch RSS"
    }

    ```

**N.B**: If you don’t have a manager account, **email us** at `worldwatch-request.ocd` AT `orange.com` to request access.

**Security tips**

Treat the **RSS API** key like a secret. Do not publish it in public repositories or client-side code.
Revoke and rotate keys if they are exposed.

---

## Response Format

Each RSS item contains metadata and content describing a security advisory.

| Field               | Notes                                  |
| ------------------- | -------------------------------------- |
| `<title>`           | Advisory title                         |
| `<link>`            | URL to advisory on the API             |
| `<description>`     | Executive summary (truncated for Free) |
| `<pubDate>`         | Publication date                       |
| `<guid>`            | Unique ID                              |
| `<severity>`        | Severity level (numeric)               |
| `<category>`        | Categories (multiple)                  |
| `<sector>`          | Sectors (multiple)                     |
| `<region>`          | Regions/Countries (multiple)           |
| `<cve>`             | CVE identifiers                        |
| `<tag>`             | Tags (multiple)                        |
| `<content:encoded>` | Full HTML content (Premium only)       |

For **Advisories**, `<category>` will contain all the `categories` of its associated **Updates** (`Content Blocks`), while `<sector>`, `<sector>`, `<region>`, `<cve>`, and `<tag>` will only contain the data **directly associated** with the advisory.

---

## Filtering

Premium feeds support filtering using query parameters.

**Logic:**

  * `OR` within a parameter (comma-separated values).
  * `AND` between different parameters

**Example:**

```js
/rss/advisories/{RSS_API_KEY}?categories=cybercrime&sectors=infrastructure,energy&countries=fr&continents=africa&tags=lapsus
```

**Interpretation:**

```js
(category=Cybercrime) AND (Infrastructure OR Energy) AND (France) AND (Africa) AND (tag=Lapsus) 
```


For **Advisories**, we will search in both **its own fields AND the fields of its content blocks**. Therefore if an advisory does not have `tag=snakedisk`, but one of its content blocks has it, the advisory will be present when filtering using that tag.

---

### Available Filters

#### Categories

|               |               |             |            |
| ------------- | ------------- | ----------- | ---------- |
| cybercriminal | ecosystem     | geopolitics | hacktivist |
| nation        | other         | technique   | threat     |
| psoa          | vulnerability | –           | –          |

---


#### Sectors

|                     | Column 2                   | Column 3               | Column 4                      | Column 5            |
| ------------------- | -------------------------- | ---------------------- | ----------------------------- | ------------------- |
| aerospace           | agriculture                | automotive             | chemical                      | commercial          |
| communications      | construction               | defense                | education                     | energy              |
| entertainment       | financial-services         | government             | government-emergency-services | government-local    |
| government-national | government-public-services | government-regional    | healthcare                    | hospitality-leisure |
| infrastructure      | infrastructure-dams        | infrastructure-nuclear | infrastructure-water          | insurance           |
| legal               | manufacturing              | mining                 | non-profit                    | pharmaceuticals     |
| retail              | technology                 | telecommunications     | transportation                | utilities           |



---

#### Countries

You can use the **Alpha-2** code for the countries. This table shows you an example of possible values:

|    |    |    |    |    |    |    |    |    |    |
| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| ar | au | at | bd | be | br | ca | ch | cn | cl |
| co | cz | de | dk | ee | eg | es | fi | fr | gb |
| hk | id | il | in | ir | jp | kz | kr | lt | lv |
| mx | ng | nl | no | nz | ph | pk | pl | ru | sa |
| se | sg | th | tr | ua | us | vn | za | –  | –  |



---

#### Continents

|                 |               |                    |                      |                |
| --------------- | ------------- | ------------------ | -------------------- | -------------- |
| africa          | americas      | asia               | australia-newzealand | caribbean      |
| central-america | central-asia  | east-asia          | eastasia             | eastern-africa |
| eastern-europe  | europe        | melanesia          | micronesia           | middle-africa  |
| middle-east     | north-america | northern-africa    | northern-europe      | oceania        |
| polynesia       | south-america | south-eastern-asia | southern-africa      | southern-asia  |
| southern-europe | west-asia     | western-africa     | western-europe       | –              |


---

#### Tags

* Any tag returned by the [`/api/tags`](https://api-ww.cert.orangecyberdefense.com/api/docs#/Tags/list_tags) endpoint is valid for filtering.
* Examples: `zunput`, `accellion`, `404tds`, etc.