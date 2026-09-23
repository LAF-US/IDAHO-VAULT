---
title: "Raising the bar for software security: GitHub 2FA begins March 13"
source: "https://github.blog/news-insights/product-news/raising-the-bar-for-software-security-github-2fa-begins-march-13/"
author:
  - "[[Laura Paine]]"
  - "[[Hirsch Singhal]]"
published: 2023-03-09
created: 2026-04-20
description: "On March 13, we will officially begin rolling out our initiative to require all developers who contribute code on GitHub.com to enable one or more forms of two-factor authentication (2FA) by the end of 2023. Read on to learn about what the process entails and how you can help secure the software supply chain with 2FA."
date created: Monday, April 20th 2026, 12:53:55 pm
date modified: Monday, April 20th 2026, 1:04:46 pm
---

Last year, we [announced our commitment](https://github.blog/2022-05-04-software-security-starts-with-the-developer-securing-developer-accounts-with-2fa/) to require all developers who contribute code on GitHub.com to enable two-factor authentication (2FA) by the end of 2023.

GitHub is central to the software supply chain, and securing the software supply chain starts with the developer. Our 2FA initiative is part of a platform-wide effort to secure software development by improving account security. Developers’ accounts are frequent targets for social engineering and account takeover (ATO). Protecting developers and consumers of the open source ecosystem from these types of attacks is the first and most critical step toward [securing the supply chain](https://github.blog/2022-03-28-how-to-secure-your-end-to-end-supply-chain-on-github/).

## From March 13, we will begin rolling out the 2FA requirement

Over the course of the next year, we’ll be reaching out to [groups of developers and administrators](https://github.blog/2022-12-14-raising-the-bar-for-software-security-next-steps-for-github-com-2fa/), starting with smaller groups on March 13, to notify them of their 2FA enrollment requirement. This gradual rollout will let us make sure developers are able to successfully onboard, and make adjustments as needed before we scale to larger groups as the year progresses.

If your account is selected for enrollment, you will be notified via email and see a banner on GitHub.com, asking you to enroll. You’ll have 45 days to configure 2FA on your account—before that date nothing will change about using GitHub except for the reminders. We’ll let you know when your enablement deadline is getting close, and once it has passed you will be required to enable 2FA the first time you access GitHub.com. You’ll have the ability to snooze this notification for up to a week, but after that your ability to access your account will be limited. Don’t worry: this snooze period only starts once you’ve signed in after the deadline, so if you’re on vacation or out of office, you’ll still get that one week period to set up 2FA when you’re back at your desk.

So, what if you’re not in an early enrollment group but you want to get started? [Click here](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa) and follow a few easy steps to enroll in 2FA.

## We’ve made it much easier to secure your GitHub account with 2FA

We want enrolling your GitHub account in 2FA to be as easy as possible, using methods that are reliable and secure so you always have access to your account (and no one else does!). To prepare for this program we’ve been busy [enhancing that experience](https://github.blog/changelog/label/authentication/). Here are a few of the highlights:

- **Second-factor validation after 2FA setup.** GitHub.com users who set up 2FA will see a prompt after 28 days, asking them to [perform 2FA and confirm their second factor settings](https://github.blog/changelog/2023-01-11-second-factor-validation-after-2fa-setup/). This prompt helps avoid account lockout due to misconfigured authenticator applications (TOTP apps). If you find that you can’t perform 2FA, you’ll be presented with a shortcut that allows you to reset your 2FA setup without being locked out of your account.
- **Enroll second factors**. Having more accessible 2FA methods is important to ensure that you *always* have access to your account. You can now have [both an authenticator app (TOTP) and an SMS number](https://github.blog/changelog/2023-03-02-sms-and-totp-can-now-both-be-registered-2fa-methods/) registered on your account at the same time. While [we recommend](https://github.blog/changelog/2022-11-21-updates-to-the-two-factor-authentication-setup-flow/) using security keys and your TOTP app over SMS, allowing both at the same time helps reduce account lock out by providing another accessible, understandable 2FA option that developers can enable.
- **Choose your preferred 2FA method.** The new [preferred option](https://github.blog/changelog/2023-02-22-preferred-2fa-methods-and-settings-improvements/) empowers you to set your preferred 2FA method for account login and use of the sudo prompt, so you’re always asked for your favorite method first during sign-in. You can choose between TOTP, SMS, security keys, or GitHub Mobile as your preferred 2FA method. We [strongly recommend](https://github.blog/changelog/2022-11-21-updates-to-the-two-factor-authentication-setup-flow/) the use of security keys and TOTPs wherever possible. SMS-based 2FA does not provide the same level of protection, and it is no longer recommended under NIST 800-63B. The strongest methods widely available are those that support the WebAuthn secure authentication standard. These methods include physical security keys, as well as personal devices that support technologies, such as Windows Hello or Face ID/Touch ID.
- **Unlink your email in case of 2FA lockout.** Since accounts on GitHub are required to have a unique email address, locked out users have difficulty starting a new account using their preferred email address—the one all their commits point to. With this feature, you can now [unlink your email address](https://github.blog/changelog/2023-02-21-unlink-your-email-in-case-of-2fa-lockout/) from a two-factor enabled GitHub account in case you’re unable to sign in or recover it. If you’re unable to find an SSH key, PAT, or a device that’s been previously signed into GitHub to recover your account, it’s easy to start fresh with a new GitHub.com account and keep that contribution graph rightfully green.

Lastly, we’re already testing [passkeys](https://fidoalliance.org/passkeys/) internally, which we believe will combine ease of use with strong, phishing-resistant authentication. Keep an eye on this space for when this functionality is ready for you.

## Reminder: what to expect if you are required to enable 2FA

GitHub has [designed a rollout process](https://github.blog/2022-12-14-raising-the-bar-for-software-security-next-steps-for-github-com-2fa/) intended to both minimize unexpected interruptions and productivity loss for users and prevent account lockouts. Groups of users will be asked to enable 2FA over time, each group selected based on the actions they’ve taken or the code they’ve contributed to.

![Timeline of the 2FA rollout process](https://github.blog/wp-content/uploads/2023/03/2fa-1.png?w=1600)

1. If you are part of a pending 2FA enablement group, you will receive notification by email informing you of your deadline to enable 2FA, as well as information on how to set up 2FA and our recommended best practices. You’ll get this email approximately 45 days before the deadline.
**More details**

\* When your group’s timeline begins, you’ll start seeing weekly reminder banners on GitHub.com, which will also guide you to the 2FA onboarding process.  
\* You’ll also receive occasional emails notifying you of your coming 2FA enablement deadline.

2\. Once the enablement deadline passes, you’ll be asked to enable 2FA the first time you access GitHub.com each day. You can snooze this prompt once a day for up to one week to provide you with flexibility, but after that week you won’t be able to access GitHub.com until you’ve enabled 2FA.

**More details**

\* This one week snooze period only starts when you access GitHub *after* the deadline, so if you’re on vacation, don’t worry–you won’t be locked out of GitHub.com.

3\. Twenty-eight (28) days after you enable 2FA, you’ll be asked to perform a 2FA check-up while using GitHub.com, which validates that your 2FA setup is working correctly. Previously signed-in users will be able to reconfigure 2FA if they have misconfigured or misplaced second factors during onboarding.

If your project takes off or you become the maintainer of a critical repository, you might suddenly qualify for a group that’s already begun their enrollment timeline. If that happens, you’ll start your 45 day period the next day, following the same timeline described above.

## Securing the software supply chain is a team effort

Open source software is ubiquitous, with [90 percent of companies reporting](https://openuk.uk/wp-content/uploads/2021/10/openuk-state-of-open_final-version.pdf) that they use open source in their proprietary software. GitHub is a critical part of the open source ecosystem, which is why we take ensuring account security seriously. Strong authentication and the use of 2FA have been recognized as best practice for many years, so we feel that GitHub has a duty to expand this best practice as part of protecting the software supply chain.

Most importantly, though, we can’t improve the security of the software supply chain without you. We thank you in advance for your support, and for enrolling your GitHub account in 2FA to make open source software more secure for all.