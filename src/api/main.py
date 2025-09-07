from urllib.parse import quote, urlencode

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.models import BuildRequest

app = FastAPI(title='LinkedIn Jobs URL Backend')


@app.get('/', include_in_schema=False)
def root() -> RedirectResponse:
    """Redirect to the interactive API documentation."""
    return RedirectResponse('/docs')


@app.get('/health', include_in_schema=False)
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {'status': 'ok'}


@app.post('/build')
async def build(req: BuildRequest) -> dict[str, str]:
    """Generate a custom LinkedIn job search URL."""
    base_url = 'https://www.linkedin.com/jobs/search'
    params = req.model_dump(by_alias=True, exclude_none=True)
    query = urlencode(params, quote_via=quote)
    return {'url': f'{base_url}?{query}' if query else base_url}
