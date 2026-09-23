---
source: "https://kb.porkbun.com/article/44-how-to-connect-domain-to-google-workspace-email"
author:
  - "[[Porkbun]]"
published: 2025-08-16
created: 2026-04-20
---
If you want to connect the domain you registered on Porkbun to Google Workspace for email hosting, you'll want to update your domain's DNS records to route mail to Google's mail servers. Luckily, Porkbun has a tool that enables you to do just that!

### Connecting Your Domain to Google Workspace

The steps to connect your Porkbun domain to Google Workspace email servers are simple. We’ve built a step-by-step guide to get you set up and ready to go in no time!

1

Log in. You should arrive at the Domain Management screen. If you're already logged in, click on ACCOUNT in the top-right corner and select Domain Management.

![](https://d33v4339jhl8k0.cloudfront.net/docs/assets/5854c918c697912ffd6c1d7a/images/685483ee64686949c258357c/file-CxJ3zd12Vm.png)

2

Locate the domain you're connecting to Google Workspace. Click the "Details" button to the far right of the domain name. On the domain details menu, locate "DNS RECORDS" and click the edit icon.

![](https://d33v4339jhl8k0.cloudfront.net/docs/assets/5854c918c697912ffd6c1d7a/images/68601f9dc48e8e0fccf135a1/file-XZLb6qKPLR.png)

3

On the "Manage DNS Records" menu that appears, scroll down until you see our "Quick DNS Config" section.

![](https://d33v4339jhl8k0.cloudfront.net/docs/assets/5854c918c697912ffd6c1d7a/images/68601fe207cc414af6e164f1/file-VvoT3QxlyS.png)

4

In the Quick DNS Config section, select the "Google Workspace" button.

![](https://d33v4339jhl8k0.cloudfront.net/docs/assets/5854c918c697912ffd6c1d7a/images/68602471c48e8e0fccf135a5/file-vJK4TlUuPq.png)

A pop-up will appear asking if you want to reconfigure your domain's DNS records. Select the "OK" button to continue.

![](https://d33v4339jhl8k0.cloudfront.net/docs/assets/5854c918c697912ffd6c1d7a/images/686024c03eb0c1274cc669ba/file-fjfNwhu5HA.png)

5

A success message will appear, letting you know that we were able to update your DNS records. You can now scroll down on the Manage DNS Records menu, and under the "Current Records" section you'll see the Google Workspace records added to your domain.

![](https://d33v4339jhl8k0.cloudfront.net/docs/assets/5854c918c697912ffd6c1d7a/images/686025b3c7a79a323c924bb5/file-TFly055MLV.png)

### Note

We have updated our Quick DNS button to reflect the [new Google Workspace MX record](https://support.google.com/a/answer/174125?hl=en#zippy=%2Cgoogle-workspace-legacy-version-before). If your Google Workspace account was created before 2023, you may have been using the "ASPMX.L.GOOGLE.COM" set of records instead, but utilizing the new "SMTP.GOOGLE.COM" record should work for these accounts as well.

Google Workspace may also provide you with an additional TXT or MX record to [verify your domain name](https://support.google.com/a/answer/60216?hl=en) with their platform. This will also need to be added in our DNS editor in addition to the Quick DNS to start using your domain name with their service. If you need any guidance on adding a DNS record to your domain manually, [check out our guide on the subject](https://kb.porkbun.com/article/231-how-to-add-dns-records-on-porkbun).

These changes may take up to 48 hours to take effect. However, in most cases, the change should be immediate, and you can start using your Google Workspace hosted email address right away.