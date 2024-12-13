import os
import aiohttp
from aiohttp import web

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp
from dotenv import load_dotenv

load_dotenv(".env")

routes = web.RouteTableDef()
router = routing.Router()

# Event handler for new issues
@router.register("issues", action="opened")
async def issue_opened_event(event, gh, *args, **kwargs): # hi
    """ Whenever an issue is opened, greet the author and say thanks. """
    url = event.data["issue"]["comments_url"]
    author = event.data["issue"]["user"]["login"]
    message = f"Thanks for the report @{author}! I will look into it ASAP! (I'm a bot)."
    await gh.post(url, data={"body": message})

# Main route to handle POST requests from GitHub
@routes.post("/")
async def main(request):
    body = await request.read()
    secret = os.environ.get("GH_SECRET")  # GitHub webhook secret
    oauth_token = os.environ.get("GH_AUTH")  # GitHub personal access token
    print(secret, oauth_token)
    # Parse the incoming webhook event
    event = sansio.Event.from_http(request.headers, body, secret=secret)
    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, "your_github_username", oauth_token=oauth_token)
        await router.dispatch(event, gh)

    return web.Response(status=200)

# Start the aiohttp webserver
if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT", 8080)  # Use port 8080 by default
    web.run_app(app, port=int(port))
