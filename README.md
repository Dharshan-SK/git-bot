# Steps:

1. Host your local port to the internet:
    ```bash
    ngrok http 8080
    ```

2. Copy the forwarding link. This will be the **"Payload URL"** for the webhook created next.

3. Go to a GitHub repository:
    - **Settings** > **Webhooks** > **Create**:
        a. Enter the **Payload URL** and select content type as `application/json`.  
        b. Enter a secret value and remember it for Step 4 (`GH_SECRET`).  
        c. Click on **"Let me select individual events"**, select **Pull actions**, and save.

4. Create a `.env` file and enter the following values:
    ```plaintext
    GH_SECRET=your_secret_value
    GH_AUTH=your_github_token
    ```

5. Change directory to the git repo and run:
    ```bash
    python -m git-bot
    ```

6. Create a new pull request. You should see a placeholder message on the pull request, and the code diff will be saved as JSON objects in the `changes` directory for further processing.
