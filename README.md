# GSuite Admin SDK Activity Scraper

# Why?

At some point, I needed to pull activity logs out of GSuite. This is not a particularly well-documented process and I could not find concrete steps to follow to get it working. Additionally, the documentation for the Admin SDK points to a deprecated library. 

After repeating the same steps half a dozen times, somehow this magically worked. So I am sharing it here to prevent others from experiencing the same frustrations I did.

# Install

```
git clone git@github.com:boboTjones/gasas.git
cd gasas
virtualenv venv
. venv/bin/activate
pip install boto3
pip install --upgrade requests
pip install --upgrade google-auth
```

# Configure GSuite/GCP/Cows

As best as I can tell, in order for this to work smoothly, you have to be a super admin on your domain. I've not written up instructions on how to do that; you can figure it out on your own. You're smart. Below are the instructions for setting up a project, a service account, granting the necessary domain-wide delegation and impersonation to the service account and authorizing the service account to access the scopes.

## Create a project: 

Browse to https://console.cloud.google.com/cloud-resource-manager. Click CREATE PROJECT. Give your project a name. Click Create. 

You should be redirect to https://console.cloud.google.com/cloud-resource-manager. Select your organization, then select your project. Click on Service Accounts in the sidebar.

## Create a service account:

Click on the button labeled Create service account. A dialog will appear. 

  - give your service account a name
  - set it to Project Viewer
  - select Furnish a new private key
  - select Enable G Suite Domain-wide Delegation
  - click CONFIGURE OAUTH CONSENT SCREEN

You will be redirected to https://console.cloud.google.com/apis/credentials/consent

  - select the email address of the super admin account that you will be impersonating
  - give your project a name (eg, GSLogScraper)
  - click Save

You will be redirected back to the Create service account screen. Click CREATE.

This will create and download a credentials file. Guard this thing as if your life depends on it because you won't be able to get another creds file with a private key in it. You will have to start over from step 4. Good luck. Once you have downloaded this file (which, btw, you should never, ever display publicly under any circumstances), click DONE.

## Authorize this service account to access scopes

You should be on the service accounts page now. If not, browse to https://console.cloud.google.com/iam-admin/serviceaccounts/project. Select your project if necessary. Click "View Client ID" next to the service account you just created. 

Open a new browser pane and paste this URL:

https://admin.google.com/latacora.com/AdminHome?chromeless=1#OGX:ManageOauthClients

Copy the client id from step 8 and paste it into the field labeled Client Name on this page. Then copy and paste the following into the field labeled One or More API Scopes:

https://www.googleapis.com/auth/admin.reports.audit.readonly,https://www.googleapis.com/auth/admin.reports.usage.readonly

Click Authorize.

## Enable the Admin SDK API

Browse to https://console.cloud.google.com/apis/dashboard. Select your project if the UI does not automatically redirect you. Click on ENABLE APIS AND SERVICES. 

Enter "admin" in the search box. Select Admin SDK. Select Admin SDK. A new page will load. Click the ENABLE button on this page.

You should now be able to access the admin api with that credentials file.
