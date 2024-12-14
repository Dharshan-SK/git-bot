# https://github-bot-tutorial.readthedocs.io/en/latest/gidgethub-for-webhooks.html#say-thanks
import os
import aiohttp
from aiohttp import web

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp
from dotenv import load_dotenv
load_dotenv(".env")

routes = web.RouteTableDef()
router = routing.Router()

@router.register("pull_request", action="opened") # https://docs.github.com/en/webhooks/webhook-events-and-payloads?actionType=edited#pull_request
async def pr_opened_event(event, gh, *args, **kwargs):
    """
    Whenever a pull request is opened, calculate the code changes and post a comment.
    """
    # Extract relevant data from the webhook payload
    pr_number = event.data["number"]
    base_repo = event.data["pull_request"]["base"]["repo"]["html_url"]
    owner = event.data["repository"]["owner"]["login"]
    repo = event.data["repository"]["name"]
    comments_url = event.data["pull_request"]["comments_url"]
    import pickle
    with open('filename.pickle', 'wb') as handle:
        pickle.dump(event, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # Fetch pull request changes using GitHub API
    changes_url = f"/repos/{owner}/{repo}/pulls/{pr_number}/files"
    changes_response = await gh.getitem(changes_url)
    
    # Calculate the total number of additions, deletions, and changes
    total_additions = 0
    total_deletions = 0
    total_changes = 0

    for i, file in enumerate(changes_response):
        import json
        os.makedirs("changes", exist_ok=True)
        json.dump(file, open(f"changes/{i}.json", "w"))
        total_additions += file["additions"]
        total_deletions += file["deletions"]
        total_changes += file["changes"]

    # Prepare the comment message
    message = (
        f"Thank you for your pull request!\n\n"
        f"Here are the details of the changes made:\n"
        f"- **Base Repository**: {base_repo}\n"
        f"- **Total Additions**: {total_additions}\n"
        f"- **Total Deletions**: {total_deletions}\n"
        f"- **Total Changes**: {total_changes}\n\n"
        f"Great job! 🚀"
    )
    
    # Post the comment to the pull request
    await gh.post(comments_url, data={"body": message})


@routes.post("/")
async def main(request):
    body = await request.read()

    # Authentication tokens
    secret = os.environ.get("GH_SECRET")
    oauth_token = os.environ.get("GH_AUTH")

    event = sansio.Event.from_http(request.headers, body, secret=secret)

    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, "your-username", oauth_token=oauth_token)
        await router.dispatch(event, gh)
    return web.Response(status=200)


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)

    web.run_app(app, port=port)
