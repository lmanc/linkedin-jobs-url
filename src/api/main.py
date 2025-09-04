from urllib.parse import quote, urlencode

from fastapi import FastAPI

from api.models import BuildRequest

app = FastAPI()


@app.post('/build')
async def build(req: BuildRequest) -> dict[str, str]:
    """Generate a custom LinkedIn job search URL."""
    base_url = 'https://www.linkedin.com/jobs/search'
    params = req.model_dump(by_alias=True, exclude_none=True)
    query = urlencode(params, quote_via=quote)
    return {'url': f'{base_url}?{query}' if query else base_url}
