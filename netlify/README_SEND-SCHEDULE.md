Netlify function: send-schedule

This site includes a Netlify Function at `netlify/functions/send-schedule.js` that sends an email with the submitted CSV attached using SendGrid.

Setup steps (Netlify):

1. Ensure the repository is deployed on Netlify. You can connect this GitHub repo to Netlify for automatic deploys.

2. Set the following environment variables in your Netlify site settings (Site settings → Build & deploy → Environment):

   - SENDGRID_API_KEY: your SendGrid API key
   - FROM_EMAIL: a verified sender email in your SendGrid account (e.g. no-reply@yourdomain.com)
   - TO_EMAIL: the recipient address (defaults to flaherty.147@osu.edu if not set)

3. Netlify will install dependencies from the repo `package.json`. We added `@sendgrid/mail` as a dependency. Netlify will install it during build. If you run locally, run:

   npm install

4. Deploy the site. The function will be available at `/.netlify/functions/send-schedule`.

Client behavior

- The `Submit schedule` button now POSTs JSON { name, email, csv } to the function.
- The function sends an email with the CSV attached and returns a JSON result.
- If the function fails, the page falls back to opening the user's default mail client with the CSV in the message body.

Security notes

- Keep `SENDGRID_API_KEY` and other secrets in Netlify environment variables only; never expose them in client-side JS.
- The function commits nothing to the repository; it only sends email. If you want to also save submissions into `submissions/` in the repo, we can extend the function to push files to the GitHub API (requires a GitHub token in env vars).
