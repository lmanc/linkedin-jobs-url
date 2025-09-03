# LinkedIn Jobs URL

- [🚀 Quick Start](#-quick-start)
- [📡 API Usage](#-api-usage)
  - [`POST /build`](#post-build)
    - [Example Request](#example-request)
    - [Example Response](#example-response)

A tiny FastAPI service that generates LinkedIn Jobs Search URLs with advanced filters.

Send a JSON payload of filters and get back a correctly encoded LinkedIn Jobs URL you can open or share.

## 🚀 Quick Start

Run:

```bash
docker compose up
```

This will build the image if needed and start the app.

## 📡 API Usage

### `POST /build`

Builds a LinkedIn jobs search URL from filters.

The schema and accepted enum values (experience levels, job types, workplace setups, sort order) are documented in the OpenAPI UI at `/docs`.

#### Example Request

```json
{
  "actively_hiring": true,
  "spell_correction": false,
  "time_range": 7200,
  "distance": 5,
  "keywords": "python backend",
  "geoId": 105685971,
  "experience_levels": [4],
  "job_types": ["F", "P"],
  "workplace_setups": [2, 3],
  "sort_by": "DD"
}
```

#### Example Response

```json
{
  "url": "https://www.linkedin.com/jobs/search?f_AL=true&spellCorrectionEnabled=false&f_TPR=r7200&distance=5&keywords=python%20backend&geoId=105685971&f_E=4&f_JT=F%2CP&f_WT=2%2C3&sortBy=DD"
}
```
