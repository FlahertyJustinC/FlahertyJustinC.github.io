# EmailJS Setup for Schedule Submissions

This page uses [EmailJS](https://www.emailjs.com) to send submitted schedules directly to your email. No backend server required — submissions are emailed to `flaherty.147@osu.edu` via EmailJS's client-side API.

## Setup Steps

### 1. Create an EmailJS Account
- Go to https://www.emailjs.com and sign up (free tier: 200 emails/month).

### 2. Add an Email Service
- In the EmailJS dashboard, go to **Email Services** and add a service (Gmail, Outlook, or custom SMTP).
- Follow their auth steps (they'll provide an app password for Gmail, etc.).
- Note your **Service ID** (e.g., `service_abc123xyz`).

### 3. Create an Email Template
- Go to **Email Templates** and create a new template.
- Use these template variables:
  ```
  {{user_name}} — {{user_email}}
  
  {{csv_content}}
  ```
- Suggested template fields:
  - **From Name**: Availability Scheduler
  - **To Email**: `{{to_email}}` (or hardcode `flaherty.147@osu.edu`)
  - **Subject**: `Availability Schedule Submission from {{user_name}}`
  - **Body**:
    ```
    Availability Schedule Submission

    Submitted by: {{user_name}}
    Email: {{user_email}}

    ========================================
    {{csv_content}}
    ========================================
    ```
- Note your **Template ID** (e.g., `template_abc123xyz`).

### 4. Get Your Public Key
- In the EmailJS dashboard, go to **Account** → **API Keys**.
- Copy your **Public Key** (e.g., `abc123xyz_public`).

### 5. Update the Availability Page
- Open `_pages/availability.html`.
- Find the lines near the top of the `<script>` section (around line 67-74):
  ```javascript
  emailjs.init('YOUR_PUBLIC_KEY');
  ```
  and replace `'YOUR_PUBLIC_KEY'` with your actual public key.

- Find the `submitSchedule()` function (around line 430) and replace:
  - `'YOUR_SERVICE_ID'` with your Service ID.
  - `'YOUR_TEMPLATE_ID'` with your Template ID.

### 6. Deploy
- Push the changes to GitHub. Your live site will now send submissions via EmailJS.

## Testing Locally
- Before deploying, you can test by:
  1. Running `bundle exec jekyll serve` locally.
  2. Opening http://localhost:4000/availability/.
  3. Filling out the form and clicking "Submit schedule".
  4. If the EmailJS keys are correct, you'll get a success alert and an email will arrive.

## Notes
- **No backend server needed** — EmailJS handles all email delivery.
- **Free tier**: 200 emails/month (upgradeable).
- **Security**: Your public key is visible in the page source, but EmailJS public keys are meant for client-side use and tied to your specific template/service.
- **Optional**: You can update the template to CC the user's email (add a CC field in the template if your EmailJS plan supports it).

## Troubleshooting
- **"Error sending email"**: Check that Service ID, Template ID, and Public Key are correct.
- **Email not arriving**: Check your EmailJS dashboard's **Logs** page to see if the API call succeeded.
- **Verify keys**: Use your emailjs dashboard — all three keys must match the template and service you created.

