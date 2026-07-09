---
source: "https://github.com/orgs/community/discussions/178128"
author:
published:
created: 2026-07-08
---
*This comprehensive guide helps you navigate GitHub's billing system, resolve common payment issues, and manage your subscriptions effectively. Whether you're troubleshooting a declined payment or trying to understand the new billing platform, you'll find step-by-step solutions here.*

## 1\. Understanding GitHub Plans & Subscriptions

### Choosing the Right Plan

GitHub offers two distinct product lines that serve different purposes:

**GitHub Platform Plans** (Free, Pro, Team, Enterprise)

- Repository hosting and collaboration features
- GitHub Actions compute minutes
- Package and storage allocation
- Advanced security and compliance tools

**GitHub Copilot Plans** (Pro, Pro+, Business, Enterprise)

- AI-powered code suggestions
- Chat and inline code assistance
- IDE and CLI integration
- Copilot is an add-on, not included in platform plans

> [!important] Important
> These are separate subscriptions. GitHub Pro does not include Copilot, and Copilot does not include GitHub Pro features.

### Quick Decision Guide

Choose your plan based on what you need:

| Your Need | Recommended Plan |
| --- | --- |
| Actions minutes, advanced collaboration | GitHub Pro ($4/month) |
| AI code suggestions and assistance | Copilot Pro ($10/month) |
| Both platform features and AI coding help | GitHub Pro + Copilot Pro |
| Team collaboration with AI coding | GitHub Team + Copilot Business |

### Feature Comparison

| Feature | GitHub Free | GitHub Pro | Copilot Pro |
| --- | --- | --- | --- |
| Public & Private repositories | ✅ Unlimited | ✅ Unlimited | N/A |
| Codespaces | 120 core hours and 15GB storage/month | 180 core hours and 20GB storage/ month | N/A |
| Actions minutes/month | 2,000 | 3,000 | N/A |
| Package storage | 500 MB | 2 GB | N/A |
| Advanced code review | ❌ | ✅ | N/A |
| AI code completion | ❌ | ❌ | ✅ |
| Chat assistance | ❌ | ❌ | ✅ |

For a complete comparison, see [GitHub's official plans documentation](https://docs.github.com/en/get-started/learning-about-github/githubs-plans) and [Billing for individual GitHub Copilot plans.](https://docs.github.com/en/copilot/concepts/billing/billing-for-individuals)

### How to Subscribe

**For GitHub Pro:**

1. Navigate to **Settings → Billing and licensing**
2. Click **Upgrade** under your current plan
3. Select **GitHub Pro** and complete payment
4. Learn more here: [Upgrading your GitHub plan](https://docs.github.com/en/billing/how-tos/manage-plan-and-licenses/upgrade-plan)

**For Copilot:**

1. Visit [github.com/github-copilot/signup](https://github.com/github-copilot/signup)
2. Choose your tier (Pro, Business, or Enterprise)
3. Complete payment with a valid payment method
4. Learn more: [Understanding Copilot licenses](https://docs.github.com/en/billing/concepts/product-billing/github-copilot-licenses)

---

## 2\. Payment Methods & Troubleshooting

### Supported Payment Methods

GitHub accepts:

- **Credit/debit cards:** Visa, Mastercard, American Express, Discover
- **PayPal:** Available in some regions

**Best Practice:** Always subscribe through **github.com in a web browser** for the most reliable experience. Mobile app purchases or third-party payment processors may charge you without activating your subscription.

### Card Declines and Failed Payments

#### Common Causes

- Insufficient funds or credit limit reached
- Bank fraud protection blocking international transactions
- Expired or incorrect card details
- Billing address mismatch with bank records
- Geographic restrictions on the card

#### Resolution Steps

1. **Verify card details:** Double-check card number, expiration date, CVV, and billing address
2. **Contact your bank:**
	- Ask them to authorize charges from "GITHUB.COM"
		- Confirm international transactions are enabled (GitHub processes through US-based systems)
		- Check if they're blocking the transaction for fraud protection
3. **Try a different card:** If issues persist, use an alternative payment method
4. **Wait between attempts:** Allow 15-30 minutes between retries to avoid triggering additional fraud blocks

To update your payment method, go to **Settings → Billing and licensing → Payment information**. Learn more: [Managing your payment method](https://docs.github.com/en/billing/how-tos/set-up-payment/manage-payment-info?versionId=free-pro-team%40latest&productId=billing&restPage=concepts%2Cproduct-billing%2Cgithub-copilot-licenses)

### Payment Processed But Subscription Not Active

This typically happens when using non-recommended payment channels:

**❌ High-Risk Methods:**

- Cryptocurrency wallets
- Third-party payment processors

**✅ Recommended Method:**

- Subscribe via **github.com** in a web browser
- Use credit/debit card or PayPal directly

#### If You're Already Charged

1. Check subscription status: **Settings → Billing and licensing**
2. Wait 10 minutes for processing
3. If still inactive, **do not purchase again**
4. Contact [GitHub Support](https://support.github.com/) with your transaction receipt
5. Support will activate your plan or process a refund

Learn more: [Troubleshooting failed payments](https://docs.github.com/en/billing/how-tos/troubleshooting)

### Authorization Holds Explained

When adding a payment method or starting a subscription, GitHub performs a temporary authorization check (typically $1-$133 USD depending on plan type). This verifies your card is valid.

**Key Facts:**

- ✅ This is not a real charge—it's a temporary hold
- ✅ The hold automatically releases within 5-7 business days
- ✅ Your actual subscription charge posts separately
- ❌ If authorization fails, your account may be temporarily locked

#### If Authorization Fails

1. Contact your bank to understand why the authorization was declined
2. Ensure sufficient available credit for the hold amount
3. Verify billing address matches your bank's records exactly
4. Once resolved, contact [GitHub Support](https://support.github.com/) to unlock your account

---

## 3\. Managing Billing Information

### Updating Your Billing Address

#### For Personal Accounts

1. Go to **Settings → Billing and licensing**
2. Click **Payment information**
3. Update your name and address fields
4. Click **Save billing information**

#### For Organizations

1. Navigate to your organization page
2. Go to **Settings → Billing and licensing**
3. Click **Edit** under **Payment information**
4. Update the name and address (you must be an organization owner)
5. Save changes

Learn more: [Adding or editing a payment method](https://docs.github.com/en/billing/managing-your-github-billing-settings/adding-or-editing-a-payment-method)

### Troubleshooting Update Issues

If you can't save billing information changes, try these solutions:

#### Common Problems and Fixes

**1\. Field Validation Errors**

| Error Message | Cause | Solution |
| --- | --- | --- |
| "Invalid billing address" | Address doesn't match bank records | Contact your bank for exact address format, then match it precisely |
| "City not recognized" | Misspelling or unsupported characters | Double-check spelling; use standard English characters only |
| "Postal code invalid" | Wrong format for your country | Verify format (US: 12345 or 12345-6789) |
| "Payment method update failed" | General processing error | Wait 10 minutes and retry |

**2\. Address Entry Best Practices**

- ✅ Match your bank records exactly (including abbreviations)
- ✅ Avoid special characters (é, ñ, ü, ™, ®, emojis)
- ✅ Use standard abbreviations (St, Ave, Apt, CA, NY)
- ✅ Double-check city spelling (Pittsburgh not Pittsburg)

**3\. Browser Issues**

Try these troubleshooting steps:

1. **Clear cache or use incognito mode:**
	- Open a private/incognito browsing window
		- Navigate to billing settings
		- Attempt the update again
2. **Try a different browser:**
	- Switch between Chrome, Firefox, Safari, or Edge
		- Temporarily disable browser extensions
3. **Use keyboard navigation:**
	- Tab through fields instead of clicking
		- Press Enter after the last field

### Removing or Changing Payment Methods

You cannot remove a payment method if you have:

- Active paid subscriptions
- Unpaid invoices or balances
- Active budgets for usage-based services

#### How to Remove a Payment Method

1. Add a new payment method first
2. Set the new method as **default**
3. Then remove the old payment method

Alternatively, cancel all paid subscriptions first, wait until the end of your billing cycle, then remove the payment method.

### When to Contact Support

Reach out to [GitHub Support](https://support.github.com/) if:

- You've tried all troubleshooting steps without success
- Your account is locked due to billing issues
- You need to update billing details but don't have access to the payment method owner
- You need help with complex organization billing

---

## 4\. Budgets & Usage Configuration

### Understanding the New Billing Platform

GitHub transitioned from **spending limits** to **budgets**, introducing important changes:

**Old System (Spending Limits):**

- Single setting for all services
- Hard cap; service stopped when limit reached

**New System (Budgets):**

- Separate budget per service (Codespaces, Actions, Packages, LFS)
- Email alerts at 75%, 100%, and 125% of budget
- You choose: pause service or allow overages
- Must be explicitly configured even if you had spending limits before

Learn more: [About the new billing platform](https://docs.github.com/en/rest/billing/billing?apiVersion=2022-11-28#about-billing)

### Why Your Codespaces or Actions Stopped Working

After the billing platform migration, usage-based services require explicit budgets before they'll work, even if you previously had spending limits configured.

**Common symptoms:**

- Codespaces won't start or show as disabled
- Actions workflows fail with billing errors
- Services inaccessible despite having a payment method on file

### Creating a Budget

#### For Personal Accounts

1. Go to **Settings → Billing and licensing**
2. Scroll to **Budgets and alerts** section
3. Click **New budget**
4. Select the service (Codespaces, Actions, Packages, or LFS)
5. Set your monthly budget amount (minimum $1)
6. Choose behavior when budget is reached:
	- **Pause service** (recommended to prevent overspending)
		- **Allow overage** (service continues; you'll be charged for additional usage)
7. Click **Create budget**

#### For Organizations

1. Navigate to organization → **Settings → Billing and licensing**
2. Go to **Budgets and alerts**
3. Follow steps 3-7 above

**Important:** Each service requires its own budget. If you use both Codespaces and Actions, create separate budgets for each.

Learn more: [Creating and editing budgets](https://docs.github.com/en/billing/tutorials/set-up-budgets?apiVersion=2022-11-28&versionId=free-pro-team%40latest&category=billing&subcategory=billing)

### Budget Troubleshooting

#### Budget Not Saving or Applying

**Troubleshooting checklist:**

1. ✅ **Verify payment method:** Go to **Settings → Billing and licensing → Payment information** and ensure a valid payment method is active
2. ✅ **Check minimum amount:** Budget must be at least $1 USD
3. ✅ **Confirm service selection:** Each budget applies to only one service
4. ✅ **Wait for activation:** Budgets can take 2-5 minutes to activate
5. ✅ **Clear cache:** Try incognito mode or a different browser

If the budget doesn't appear after 10 minutes, contact [GitHub Support](https://support.github.com/) with the service name, budget amount, and any error messages.

### Understanding Budget Mechanics

| Feature | Details |
| --- | --- |
| **Scope** | Per service (one budget each for Codespaces, Actions, Packages, LFS) |
| **Period** | Monthly (resets on billing cycle date) |
| **Alerts** | Email notifications at 75%, 100%, and 125% of budget |
| **Charges** | You're only charged for actual usage, not the budget amount |

**Example:** Setting a $50 budget doesn't mean you'll be charged $50. It's a spending limit, not a subscription fee. If you only use $20 worth of services, you only pay $20.

### Monitoring Usage

Check current usage against your budget:

- Go to **Settings → Billing and Licensing → Usage this month**
- View real-time consumption for each service
- Download usage reports for detailed analysis

[Learn more about setting up budgets to control spendings](https://docs.github.com/en/billing/tutorials/set-up-budgets)

---

## 5\. Canceling Subscriptions

### Using the Virtual Assistant (GitHub Pro)

For quick cancellations:

1. Visit [GitHub Support](https://support.github.com/contact-next?tags=hubberfy_billing_and_payments) ([https://support.github.com/contact-next](https://support.github.com/contact-next))
2. **Select An Account**
3. Continue
4. Follow the virtual assistant's guidance
5. Available 24/7 for instant help

**After cancellation:**

- You keep access until the end of your current billing period
- No refund for unused time
- You can re-subscribe anytime

> [!note] Note
> Cancelling subscriptions via the Virtual Assistant is only for Copilot Pro subscriptions and refunds are automatically issued in the VA.

Learn more: [Canceling your Copilot subscription](https://docs.github.com/en/copilot/how-tos/manage-your-account/view-and-change-your-copilot-plan)

### Downgrading GitHub Pro/Team

**For Personal Accounts (GitHub Pro):**

1. Go to **Settings → Billing and licensing**
2. Click **Edit** next to your plan
3. Select **Downgrade to Free**
4. Confirm downgrade

**For Organizations (Team):**

1. Go to organization → **Settings → Billing and licensing**
2. Click **Edit** next to your plan
3. Select **Downgrade** or **Cancel**
4. Confirm (requires organization owner permissions)

**What you'll lose:**

- Advanced features (required reviewers, code owners, etc.)
- Increased Actions minutes and storage
- Private repositories may become public if over Free plan limits

Learn more: [Downgrading your GitHub subscription](https://docs.github.com/en/billing/how-tos/manage-plan-and-licenses/downgrade-plan)

### Stopping Usage-Based Services

To stop charges for Codespaces, Actions, or Packages:

**Stop All Charges:**

1. Go to **Settings → Billing and licensing → Budgets**
2. Find the service budget
3. Click **Delete budget** or set to **pause service at limit**

**For Codespaces Specifically:**

- Delete all active codespaces at [github.com/codespaces](https://github.com/codespaces)
- Remove the Codespaces budget
- Disable automatic creation in repository settings

### Cancellation Timing and Refunds

| Subscription Type | When Access Ends | Refund Policy |
| --- | --- | --- |
| Copilot Pro | End of billing period | No |
| GitHub Pro | Immediate downgrade | Prorated credit may apply |
| Team | End of billing period | Contact sales |
| Usage-based services | Immediately | Charged only for actual usage |

**Check your next billing date:** Go to **Settings → Billing and licensing → Overview** to see when your current period ends.

### Pre-Cancellation Checklist

Before canceling, remember to:

- Backup important data (repositories, issues, discussions)
- Review collaborator access impacts
- Check private repository status
- Download invoices for your records
- Cancel related budgets and services
- Note your renewal date

---

## Frequently Asked Questions

### General Billing Questions

Details \*\*Q: How do I know which plan I currently have?\*\* A: Go to \*\*Settings → Billing and licensing → Overview\*\*. Your current plan is displayed at the top, along with all active subscriptions.

**Q: Can I have both GitHub Pro and Copilot Pro?**  
A: Yes. They are separate subscriptions that can be combined. You can subscribe to GitHub Pro for platform features and Copilot Pro for AI assistance.

**Q: When does my billing cycle start?**  
A: Your billing cycle starts on the date you first subscribed and repeats monthly. Check **Settings → Billing and licensing** to see your next billing date.

Metered products have a fixed billing period that starts at 00:00:00 UTC on the first day of each month and ends at 23:59:59 UTC on the last day of the month. [More information here](https://docs.github.com/en/billing/concepts/billing-cycles?versionId=free-pro-team%40latest&productId=billing&restPage=how-tos%2Ctroubleshooting%2Clocked-account)

At the end of each month, your metered usage is calculated and scheduled to be billed on your bill cycle day.

**Q: Does GitHub offer annual billing?**  
A: Yes, for some plans. Annual billing is available for GitHub Pro, Team, and Enterprise plans, often at a discounted rate. Copilot Pro and Pro+ is also available at a discounted rate. [More information here](https://docs.github.com/en/copilot/get-started/plans#comparing-copilot-plans)

Also, sponsorships can be added to a subscription on a monthly or annual basis, depending on the existing account billing cadence. So, if you pay for GitHub Pro annually and add a sponsorship, the sponsorship will also be billed annually.

**Q: Can I get a refund if I cancel?**  
A: Generally, GitHub does not provide refunds for unused time. You maintain access until the end of your paid billing period after canceling.

### Payment and Security

Details \*\*Q: Is it safe to enter my credit card on GitHub?\*\* A: Yes. GitHub uses industry-standard encryption and PCI-compliant payment processing. Your payment information is never stored directly on GitHub's servers.

**Q: Why does GitHub charge $1 to my card?**  
A: This is a temporary authorization hold to verify your card is valid. It's not an actual charge and will disappear from your statement within 5-7 business days.

**Q: Can I use prepaid cards or gift cards?**  
A: Some prepaid cards work if they support recurring billing and international transactions. However, regular credit or debit cards are more reliable.

**Q: My card keeps getting declined. What should I do?**  
A: Contact your bank first, they may be blocking international transactions or flagging GitHub as suspicious. Ask them to authorize charges from "GITHUB.COM" and ensure your billing address matches their records.

**Q: Can I split payment across multiple cards?**  
A: No. Each subscription requires a single payment method. However, you can use different cards for different subscriptions (e.g., one card for GitHub Pro, another for Copilot).

### Budgets and Usage

Details

**Q: Do I need a budget if I'm on the Free plan?**  
A: Only if you want to use paid features like Codespaces, additional Actions minutes, or Packages beyond the free tier.

**Q: What happens when I reach my budget limit?**  
A: It depends on your setting:

- **Pause service:** Codespaces won't start, Actions workflows stop
- **Allow overage:** Services continue and you pay for additional usage

**Q: Can I set a $0 budget to prevent all charges?**  
A: No. The minimum budget is $1. To prevent charges entirely, delete the budget instead.

**Q: How do I check my current usage?**  
A: Go to **Settings → Billing and licensing → Usage this month** for real-time consumption data across all services.

**Q: I had a spending limit before. Where did it go?**  
A: GitHub migrated from spending limits to budgets. You need to create new budgets for each service you use (Codespaces, Actions, Packages).

**Q: Will I be charged the full budget amount every month?**  
A: No. You're only charged for what you actually use. The budget is a spending cap, not a subscription fee.

### Plan and Subscription Changes

Details

**Q: Can I switch from monthly to annual billing?**  
A: Yes. Go to **Settings → Billing and licensing**, click **Edit** next to your plan, and select annual billing. You'll be charged for the full year immediately.

**Q: What happens to my private repositories if I downgrade from Pro to Free?**  
A: You keep all private repositories. However, if you have more collaborators than the Free plan allows, you'll need to adjust access.

**Q: Can I pause my subscription instead of canceling?**  
A: No. GitHub doesn't offer subscription pausing. You must cancel and lose access at the end of the billing period, then re-subscribe when ready.

**Q: If I cancel Copilot, can I reactivate it later?**  
A: Yes. You can re-subscribe to Copilot anytime. You'll start a new billing cycle from the reactivation date.

**Q: How do I upgrade from Pro to Business Copilot?**  
A: Cancel your Pro subscription, wait for it to expire, then subscribe to Copilot Business through your organization settings.

### Troubleshooting

Details

**Q: My subscription shows as active but I don't have access. Why?**  
A: This can happen if:

- Payment failed after initial activation (check payment method)
- You need to sign out and back in to refresh permissions
- Your organization owner hasn't assigned you a seat (for Business plans)
- There's a temporary service issue (check [GitHub Status](https://www.githubstatus.com/))

**Q: I was charged twice. What should I do?**  
A: Contact [GitHub Support](https://support.github.com/) immediately with both transaction IDs. Double charges typically happen when:

- You have subscriptions on multiple accounts
- A payment retry succeeded after an initial failure
- You upgraded mid-cycle

**Q: My Codespaces stopped working suddenly. What happened?**  
A: Most likely you need to create a budget. After GitHub's billing platform migration, Codespaces requires an explicit budget. Go to **Settings → Billing and licensing → Budgets** and create a Codespaces budget.

**Q: I can't update my billing address. What's wrong?**  
A: Common causes:

- Misspelled city name
- Billing address doesn't match your bank's records
- Special characters in address fields
- Browser cache or extension conflicts

Try incognito mode, double-check spelling, and ensure the address matches your bank exactly.

**Q: How do I remove my payment method?**  
A: You can only remove a payment method if you have no active paid subscriptions or outstanding balances. Cancel all subscriptions first, wait until the end of the billing period, then remove the payment method.

### Organization Billing

Details \*\*Q: Who can manage billing for an organization?\*\* A: Only organization owners can access and modify billing settings, including payment methods, plans, and budgets.

**Q: Can I have separate billing for different teams in my organization?**  
A: No. Organizations have a single billing profile. All services and subscriptions roll up to one payment method and invoice.

**Q: How do I add billing managers without making them organization owners?**  
A: You can add billing managers by going to **Organization Settings → Billing and licensing → Billing managers** and inviting users. They can view billing information and download invoices but can't make changes.

**Q: Can I split an organization subscription cost among team members?**  
A: GitHub bills the organization directly. How you split costs internally is up to your team's financial arrangements—GitHub doesn't facilitate cost-sharing.

### Support and Resources

Details \*\*Q: How do I contact GitHub Support about billing?\*\* A: Visit \[GitHub Support\](https://support.github.com) and either use the virtual assistant or click "Contact Support" to reach a human agent. Have your account name and any relevant transaction IDs ready.

**Q: Where can I download my invoices?**  
A: Go to **Settings → Billing and licensing → Payment history**. Click on any past payment to download the invoice PDF.

**Q: How long does GitHub Support take to respond?**  
A: Response times vary:

- Virtual assistant: Immediate
- Email support: Usually within 3 to 5 business days
- Enterprise customers: Faster response based on support tier

**Q: Can I talk to someone on the phone about billing?**  
A: GitHub handles billing support through their online support portal. Phone support is only available for Premium Support customers via GitHub Enterprise platform plan. [More information here](https://docs.github.com/en/enterprise-cloud@latest/support/learning-about-github-support/about-github-support)

---

## Quick Reference: Preventing Common Billing Issues

Follow these best practices to avoid common problems:

1. ✅ **Always subscribe via github.com in a web browser**
2. ✅ **Create budgets immediately** for any usage-based services (Codespaces, Actions, Packages)
3. ✅ **Match billing addresses exactly** to your bank records when updating payment info
4. ✅ **Understand plan differences** before subscribing (Pro ≠ Copilot)
5. ✅ **Use the virtual assistant** at [support.github.com](https://support.github.com/) for quick help
6. ✅ **Keep payment methods current** and set reminders before card expiration
7. ✅ **Enable billing email notifications** for payment failures and budget alerts
8. ✅ **Review billing settings monthly** to catch issues early

## Additional Resources

**Official Documentation:**

- [GitHub Billing Documentation](https://docs.github.com/en/billing)
- [GitHub Plans Overview](https://docs.github.com/en/get-started/learning-about-github/githubs-plans)

**Support:**

- [GitHub Support Portal](https://support.github.com/)
- [GitHub Community Discussions](https://github.com/orgs/community/discussions/categories/general?discussions_q=is%3Aopen+category%3AGeneral+label%3Abilling)
- [GitHub Status](https://www.githubstatus.com/)

**Copilot:**

- [Requests in GitHub Copilot](https://docs.github.com/en/copilot/concepts/billing/copilot-requests)
- [About billing for individual GitHub Copilot plans](https://docs.github.com/en/copilot/concepts/billing/billing-for-individuals#about-premium-requests)

*This guide is community-maintained and based on common billing issues and questions. For the most up-to-date information, always refer to [GitHub's official documentation](https://docs.github.com/en/billing). Last updated Oct, 2025*

### This comment was marked as off-topic.

Show comment

Hide comment

#### smart432345

Hello everyone! Hope you’re having a great day. I just wanted to share my thoughts on this topic and be part of the discussion.

### This comment was marked as off-topic.

Show comment

Hide comment

#### shba8271-lab

gh repo clone tronscan/tron-tvc-list  
[![Order ID(USDU2511110443170241)1762807912346](https://private-user-images.githubusercontent.com/241380268/512394623-51ed8f2c-0b4a-41ff-a128-4c5675655880.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODM1NDkxODUsIm5iZiI6MTc4MzU0ODg4NSwicGF0aCI6Ii8yNDEzODAyNjgvNTEyMzk0NjIzLTUxZWQ4ZjJjLTBiNGEtNDFmZi1hMTI4LTRjNTY3NTY1NTg4MC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNzA4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDcwOFQyMjE0NDVaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT00YzhlNjc1MGMxNjlhZWY2NjUzZGMxMmIyYTRkMTA3ZGIyZWY3ZGNkY2Q5ZmQzOGMyODM1MGZhODQ2NzUzOWIxJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZwbmcifQ.T8Oyulyc9mNV95Gwda1zSonQ5117e2oEpxPiyF3sX0A)](https://private-user-images.githubusercontent.com/241380268/512394623-51ed8f2c-0b4a-41ff-a128-4c5675655880.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODM1NDkxODUsIm5iZiI6MTc4MzU0ODg4NSwicGF0aCI6Ii8yNDEzODAyNjgvNTEyMzk0NjIzLTUxZWQ4ZjJjLTBiNGEtNDFmZi1hMTI4LTRjNTY3NTY1NTg4MC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNzA4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDcwOFQyMjE0NDVaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT00YzhlNjc1MGMxNjlhZWY2NjUzZGMxMmIyYTRkMTA3ZGIyZWY3ZGNkY2Q5ZmQzOGMyODM1MGZhODQ2NzUzOWIxJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZwbmcifQ.T8Oyulyc9mNV95Gwda1zSonQ5117e2oEpxPiyF3sX0A)

### This comment was marked as off-topic.

Show comment

Hide comment

#### peansokchann431-bit

PEANSOKCHANN

### This comment was marked as off-topic.

Show comment

Hide comment

#### maheryymaheree-byte

01677911135

### This comment was marked as duplicate.

Show comment

Hide comment

#### maheryymaheree-byte

> Hello everyone! Hope you’re having a great day. I just wanted to share my thoughts on this topic and be part of the discussion.

### This comment was marked as off-topic.

Show comment

Hide comment

#### coper015

The GitHub Community Discussions Billing & Subscription Guide provides clear help on managing your GitHub payments, including how to view invoices, update billing details, change subscriptions, cancel plans, and troubleshoot common payment issues.

[paymydoctor](https://uspaymydoctor.online/)

### This comment was marked as off-topic.

Show comment

Hide comment

#### faizanmazhar0202-maker

I want to develop an appp\_

### This comment was marked as off-topic.

Show comment

Hide comment

#### Whatsplusap

The GitHub Community Discussions Billing & Subscription Guide explains how billing works for users and organizations on the platform. While Discussions is free for public repositories, private or enterprise use may fall under paid plans. Account owners can manage payments, invoices, and upgrades in billing settings. For teams using GitHub to collaborate on projects, including those related to a [messaging modified platform](https://github.com/orgs/community/discussions/whatsplusap.com), proper billing management ensures smooth access, advanced features, and uninterrupted workflow.

### This comment was marked as off-topic.

Show comment

Hide comment

#### granjacours410-source

They messing whit my id.whit the bank whit my gouverment. Going on my name loans open bankaccounts.they putting my in deep shit

### Zaidux on Nov 11, 2025

Hi GitHub Team,  
I hope this message finds you well. I wanted to share a small suggestion regarding your AI subscription plans.  
First of all, I want to say that your AI features are incredibly helpful — especially for developers like myself.

However, I noticed that the available plans are limited to monthly and yearly options. I believe introducing more flexible pricing could make a real difference for users with varying budgets around the world.

I’d like to suggest two possible additions:

A $3 monthly plan with more limited access or restrictions.

A $3 weekly plan offering full access similar to the $10 subscription.

The idea behind this is to provide flexibility and accessibility. GitHub is a global platform with users from regions where currency conversion rates and income levels differ significantly.

For many, even small adjustments in pricing can determine whether they can access these powerful tools or not.

This approach could help reduce entry barriers, attract a broader user base, and ultimately benefit both GitHub and its community.

Thank you for taking the time to consider this suggestion. I appreciate all the work you’re doing to support developers worldwide.

Warm regards,  
Zaidu Abubakar

0 replies

### This comment was marked as off-topic.

Show comment

Hide comment

#### BENZERSIZKD

I have problem with my subscription and I have a ticket on Support before 48 hours. But nothing change!  
I want to get a help please! I need to use my copilot pro but it still seems free!

Can anybody help me via Support??

[https://support.github.com/ticket/personal/0/3891733](https://support.github.com/ticket/personal/0/3891733)

### libreosley-founder on Nov 12, 2025

I just started using GitHub Copilot on the free plan and hit it's limit's so went to upgrade did the form filling and selected the trial on the $10 monthly and it clearly said the first $10 will be taken in December 2025 so OK grate completed the order went back to my VSCode where I'm using GitHub Copilot after a refresh all good for one message then it stopped then I got a message on my phone from my bank GitHub tried to take $10 today now the question is why and can you be trusted with storing card details if you are just going to go back on your word of when you will charge or was which one is right the offer message and first payment is in December or we pay from day one and a hold on a card payment only last for 3 to 5 days and not 30 day's so it could not of been a hold as they are for mainly card check that's all so what is it?

2 replies

#### caiquemoa on Nov 13, 2025

same here did u solve it?

### This comment was marked as off-topic.

Show comment

Hide comment

#### singaporelovegaza-ship-it

هل هناك مشكلة

### caiquemoa on Nov 13, 2025

i tested it in my pc for a day and it said my monthly quota has ended and saw a promotion subscrible for 10doll a month and get a free trial of 30 days after subscription i try to use the copilot it said my 30 days have already ended all this in 3min and now the free trial option do not appear anymore and now i dont know if i should trust github support because they don't provide any

0 replies

### KP-AOT on Nov 19, 2025

Hi there,

Our company is on the Free GitHub plan but we have an add-on subscription for GitHub Copilot Business, which we purchased directly through GitHub. We have been charged for the Copilot Business subscription; however, no invoice was sent to our billing email, nor is any invoice available under the Payment History in either our organization account or my personal account.

I submitted a support ticket two weeks ago but have not received any response. We urgently need the invoice for our accounting records. Could you advise what steps we should take, or assist us in obtaining the invoice?

Thank you.

1 reply

#### chisomofulagha140-del on Nov 22, 2025

I'm ready sorry for the late responses because I wasn't able to access my Gmail account [josephofulagha@gmail.com](mailto:josephofulagha@gmail.com). but I can now and I honestly thank you and the lovely community for your kind patients towards me. It's really an honor. Must Respect;!!

### chisomofulagha140-del on Nov 22, 2025

I will try my best to get the invoice but I would love this lovely community to also help me out because it's really been along ride for me trying to recover my Gmail

0 replies

### This comment was marked as off-topic.

Show comment

Hide comment

#### ABDULLA326

شكراً!

### This comment was marked as off-topic.

Show comment

Hide comment

#### singaporelovegaza-ship-it

### libreosley-founder on Nov 25, 2025

No, also to top this yesterday I loaded GitHub Copilot into VSCode and loaded local installed ollama and found it was crashing which was odd as all i was asking it was "hi" and when looking into it GitHub Copilot was sending 9K of Tokens just for a message of "hi" so have stopped using VSCode and GitHub Copilot totallyand having looked into this more have found out that end user's token usage is not just what tokens size there message is but also the size of all the rules the provider (GitHub Copilot) set's hence the 9K of tokens just for a "hi" so what would it be on a fully message and if I was using an cloud AI Model using a pay-per-usage API call that would cost load. so GitHub Copilot has to answer why they are sending so many tokens on each and every call/message. and until that happens i will only use local self-hosted model's even if the work take longer to get done

[…](#)

On Thu, 13 Nov 2025 at 19:15, Carlos Henrique \*\*\*@\*\*\*.\*\*\*> wrote: same here did u solve it? — Reply to this email directly, view it on GitHub < [#178128 (reply in thread)](https://github.com/orgs/community/discussions/178128#discussioncomment-14961973) >, or unsubscribe < [https://github.com/notifications/unsubscribe-auth/BVVGWYC6CPMVII7IWU4JKMD34TKFVAVCNFSM6AAAAACKKL5UGWVHI2DSMVQWIX3LMV43URDJONRXK43TNFXW4Q3PNVWWK3TUHMYTIOJWGE4TOMY](https://github.com/notifications/unsubscribe-auth/BVVGWYC6CPMVII7IWU4JKMD34TKFVAVCNFSM6AAAAACKKL5UGWVHI2DSMVQWIX3LMV43URDJONRXK43TNFXW4Q3PNVWWK3TUHMYTIOJWGE4TOMY) >. You are receiving this because you commented.Message ID: \*\*\*@\*\*\*.\*\*\*>

0 replies

### This comment was marked as off-topic.

Show comment

Hide comment

#### nashirtalukder17-png

here

### This comment was marked as duplicate.

Show comment

Hide comment

#### beaconchain-horizon

> *This comprehensive guide helps you navigate GitHub's billing system, resolve common payment issues, and manage your subscriptions effectively. Whether you're troubleshooting a declined payment or trying to understand the new billing platform, you'll find step-by-step solutions here.*
> 
> ## Table of Contents
> 
> 1. [Understanding GitHub Plans & Subscriptions](#1-understanding-github-plans--subscriptions)
> 2. [Payment Methods & Troubleshooting](#2-payment-methods--troubleshooting)
> 3. [Managing Billing Information](#3-managing-billing-information)
> 4. [Budgets & Usage Configuration](#4-budgets--usage-configuration)
> 5. [Canceling Subscriptions](#5-canceling-subscriptions)
> 6. [Frequently Asked Questions](#6-frequently-asked-questions)
> 
> ## 1\. Understanding GitHub Plans & Subscriptions
> 
> ### Choosing the Right Plan
> 
> GitHub offers two distinct product lines that serve different purposes:  
> **GitHub Platform Plans** (Free, Pro, Team, Enterprise)
> 
> - Repository hosting and collaboration features
> - GitHub Actions compute minutes
> - Package and storage allocation
> - Advanced security and compliance tools
> 
> **GitHub Copilot Plans** (Pro, Pro+, Business, Enterprise)
> 
> - AI-powered code suggestions
> - Chat and inline code assistance
> - IDE and CLI integration
> - Copilot is an add-on, not included in platform plans
> 
> Important  
> These are separate subscriptions. GitHub Pro does not include Copilot, and Copilot does not include GitHub Pro features.
> 
> ### Quick Decision Guide
> 
> Choose your plan based on what you need:  
> Your Need Recommended Plan  
> Actions minutes, advanced collaboration GitHub Pro ($4/month)  
> AI code suggestions and assistance Copilot Pro ($10/month)  
> Both platform features and AI coding help GitHub Pro + Copilot Pro  
> Team collaboration with AI coding GitHub Team + Copilot Business
> 
> ### Feature Comparison
> 
> Feature GitHub Free GitHub Pro Copilot Pro  
> Public & Private repositories ✅ Unlimited ✅ Unlimited N/A  
> Codespaces 120 core hours and 15GB storage/month 180 core hours and 20GB storage/ month N/A  
> Actions minutes/month 2,000 3,000 N/A  
> Package storage 500 MB 2 GB N/A  
> Advanced code review ❌ ✅ N/A  
> AI code completion ❌ ❌ ✅  
> Chat assistance ❌ ❌ ✅  
> For a complete comparison, see [GitHub's official plans documentation](https://docs.github.com/en/get-started/learning-about-github/githubs-plans) and [Billing for individual GitHub Copilot plans.](https://docs.github.com/en/copilot/concepts/billing/billing-for-individuals)
> 
> ### How to Subscribe
> 
> **For GitHub Pro:**
> 
> 1. Navigate to **Settings → Billing and licensing**
> 2. Click **Upgrade** under your current plan
> 3. Select **GitHub Pro** and complete payment
> 4. Learn more here: [Upgrading your GitHub plan](https://docs.github.com/en/billing/how-tos/manage-plan-and-licenses/upgrade-plan)
> 
> **For Copilot:**
> 
> 1. Visit [github.com/github-copilot/signup](https://github.com/github-copilot/signup)
> 2. Choose your tier (Pro, Business, or Enterprise)
> 3. Complete payment with a valid payment method
> 4. Learn more: [Understanding Copilot licenses](https://docs.github.com/en/billing/concepts/product-billing/github-copilot-licenses)
> 
> ## 2\. Payment Methods & Troubleshooting
> 
> ### Supported Payment Methods
> 
> GitHub accepts:
> 
> - **Credit/debit cards:** Visa, Mastercard, American Express, Discover
> - **PayPal:** Available in some regions
> 
> **Best Practice:** Always subscribe through **github.com in a web browser** for the most reliable experience. Mobile app purchases or third-party payment processors may charge you without activating your subscription.
> 
> ### Card Declines and Failed Payments
> 
> #### Common Causes
> 
> - Insufficient funds or credit limit reached
> - Bank fraud protection blocking international transactions
> - Expired or incorrect card details
> - Billing address mismatch with bank records
> - Geographic restrictions on the card
> 
> #### Resolution Steps
> 
> 1. **Verify card details:** Double-check card number, expiration date, CVV, and billing address
> 2. **Contact your bank:**
> 	- Ask them to authorize charges from "GITHUB.COM"
> 		- Confirm international transactions are enabled (GitHub processes through US-based systems)
> 		- Check if they're blocking the transaction for fraud protection
> 3. **Try a different card:** If issues persist, use an alternative payment method
> 4. **Wait between attempts:** Allow 15-30 minutes between retries to avoid triggering additional fraud blocks
> 
> To update your payment method, go to **Settings → Billing and licensing → Payment information**. Learn more: [Managing your payment method](https://docs.github.com/en/billing/how-tos/set-up-payment/manage-payment-info?versionId=free-pro-team%40latest&productId=billing&restPage=concepts%2Cproduct-billing%2Cgithub-copilot-licenses)
> 
> ### Payment Processed But Subscription Not Active
> 
> This typically happens when using non-recommended payment channels:  
> **❌ High-Risk Methods:**
> 
> - Cryptocurrency wallets
> - Third-party payment processors
> 
> **✅ Recommended Method:**
> 
> - Subscribe via **github.com** in a web browser
> - Use credit/debit card or PayPal directly
> 
> #### If You're Already Charged
> 
> 1. Check subscription status: **Settings → Billing and licensing**
> 2. Wait 10 minutes for processing
> 3. If still inactive, **do not purchase again**
> 4. Contact [GitHub Support](https://support.github.com/) with your transaction receipt
> 5. Support will activate your plan or process a refund
> 
> Learn more: [Troubleshooting failed payments](https://docs.github.com/en/billing/how-tos/troubleshooting)
> 
> ### Authorization Holds Explained
> 
> When adding a payment method or starting a subscription, GitHub performs a temporary authorization check (typically $1-$133 USD depending on plan type). This verifies your card is valid.  
> **Key Facts:**
> 
> - ✅ This is not a real charge—it's a temporary hold
> - ✅ The hold automatically releases within 5-7 business days
> - ✅ Your actual subscription charge posts separately
> - ❌ If authorization fails, your account may be temporarily locked
> 
> #### If Authorization Fails
> 
> 1. Contact your bank to understand why the authorization was declined
> 2. Ensure sufficient available credit for the hold amount
> 3. Verify billing address matches your bank's records exactly
> 4. Once resolved, contact [GitHub Support](https://support.github.com/) to unlock your account
> 
> ## 3\. Managing Billing Information
> 
> ### Updating Your Billing Address
> 
> #### For Personal Accounts
> 
> 1. Go to **Settings → Billing and licensing**
> 2. Click **Payment information**
> 3. Update your name and address fields
> 4. Click **Save billing information**
> 
> #### For Organizations
> 
> 1. Navigate to your organization page
> 2. Go to **Settings → Billing and licensing**
> 3. Click **Edit** under **Payment information**
> 4. Update the name and address (you must be an organization owner)
> 5. Save changes
> 
> Learn more: [Adding or editing a payment method](https://docs.github.com/en/billing/managing-your-github-billing-settings/adding-or-editing-a-payment-method)
> 
> ### Troubleshooting Update Issues
> 
> If you can't save billing information changes, try these solutions:
> 
> #### Common Problems and Fixes
> 
> **1\. Field Validation Errors**  
> Error Message Cause Solution  
> "Invalid billing address" Address doesn't match bank records Contact your bank for exact address format, then match it precisely  
> "City not recognized" Misspelling or unsupported characters Double-check spelling; use standard English characters only  
> "Postal code invalid" Wrong format for your country Verify format (US: 12345 or 12345-6789)  
> "Payment method update failed" General processing error Wait 10 minutes and retry  
> **2\. Address Entry Best Practices**
> 
> - ✅ Match your bank records exactly (including abbreviations)
> - ✅ Avoid special characters (é, ñ, ü, ™, ®, emojis)
> - ✅ Use standard abbreviations (St, Ave, Apt, CA, NY)
> - ✅ Double-check city spelling (Pittsburgh not Pittsburg)
> 
> **3\. Browser Issues**  
> Try these troubleshooting steps:
> 
> 1. **Clear cache or use incognito mode:**
> 	- Open a private/incognito browsing window
> 		- Navigate to billing settings
> 		- Attempt the update again
> 2. **Try a different browser:**
> 	- Switch between Chrome, Firefox, Safari, or Edge
> 		- Temporarily disable browser extensions
> 3. **Use keyboard navigation:**
> 	- Tab through fields instead of clicking
> 		- Press Enter after the last field
> 
> ### Removing or Changing Payment Methods
> 
> You cannot remove a payment method if you have:
> 
> - Active paid subscriptions
> - Unpaid invoices or balances
> - Active budgets for usage-based services
> 
> #### How to Remove a Payment Method
> 
> 1. Add a new payment method first
> 2. Set the new method as **default**
> 3. Then remove the old payment method
> 
> Alternatively, cancel all paid subscriptions first, wait until the end of your billing cycle, then remove the payment method.
> 
> ### When to Contact Support
> 
> Reach out to [GitHub Support](https://support.github.com/) if:
> 
> - You've tried all troubleshooting steps without success
> - Your account is locked due to billing issues
> - You need to update billing details but don't have access to the payment method owner
> - You need help with complex organization billing
> 
> ## 4\. Budgets & Usage Configuration
> 
> ### Understanding the New Billing Platform
> 
> GitHub transitioned from **spending limits** to **budgets**, introducing important changes:  
> **Old System (Spending Limits):**
> 
> - Single setting for all services
> - Hard cap; service stopped when limit reached
> 
> **New System (Budgets):**
> 
> - Separate budget per service (Codespaces, Actions, Packages, LFS)
> - Email alerts at 75%, 100%, and 125% of budget
> - You choose: pause service or allow overages
> - Must be explicitly configured even if you had spending limits before
> 
> Learn more: [About the new billing platform](https://docs.github.com/en/rest/billing/billing?apiVersion=2022-11-28#about-billing)
> 
> ### Why Your Codespaces or Actions Stopped Working
> 
> After the billing platform migration, usage-based services require explicit budgets before they'll work, even if you previously had spending limits configured.  
> **Common symptoms:**
> 
> - Codespaces won't start or show as disabled
> - Actions workflows fail with billing errors
> - Services inaccessible despite having a payment method on file
> 
> ### Creating a Budget
> 
> #### For Personal Accounts
> 
> 1. Go to **Settings → Billing and licensing**
> 2. Scroll to **Budgets and alerts** section
> 3. Click **New budget**
> 4. Select the service (Codespaces, Actions, Packages, or LFS)
> 5. Set your monthly budget amount (minimum $1)
> 6. Choose behavior when budget is reached:
> 	- **Pause service** (recommended to prevent overspending)
> 		- **Allow overage** (service continues; you'll be charged for additional usage)
> 7. Click **Create budget**
> 
> #### For Organizations
> 
> 1. Navigate to organization → **Settings → Billing and licensing**
> 2. Go to **Budgets and alerts**
> 3. Follow steps 3-7 above
> 
> **Important:** Each service requires its own budget. If you use both Codespaces and Actions, create separate budgets for each.  
> Learn more: [Creating and editing budgets](https://docs.github.com/en/billing/tutorials/set-up-budgets?apiVersion=2022-11-28&versionId=free-pro-team%40latest&category=billing&subcategory=billing)
> 
> ### Budget Troubleshooting
> 
> #### Budget Not Saving or Applying
> 
> **Troubleshooting checklist:**
> 
> 1. ✅ **Verify payment method:** Go to **Settings → Billing and licensing → Payment information** and ensure a valid payment method is active
> 2. ✅ **Check minimum amount:** Budget must be at least $1 USD
> 3. ✅ **Confirm service selection:** Each budget applies to only one service
> 4. ✅ **Wait for activation:** Budgets can take 2-5 minutes to activate
> 5. ✅ **Clear cache:** Try incognito mode or a different browser
> 
> If the budget doesn't appear after 10 minutes, contact [GitHub Support](https://support.github.com/) with the service name, budget amount, and any error messages.
> 
> ### Understanding Budget Mechanics
> 
> Feature Details  
> **Scope** Per service (one budget each for Codespaces, Actions, Packages, LFS)  
> **Period** Monthly (resets on billing cycle date)  
> **Alerts** Email notifications at 75%, 100%, and 125% of budget  
> **Charges** You're only charged for actual usage, not the budget amount  
> **Example:** Setting a $50 budget doesn't mean you'll be charged $50. It's a spending limit, not a subscription fee. If you only use $20 worth of services, you only pay $20.
> 
> ### Monitoring Usage
> 
> Check current usage against your budget:
> 
> - Go to **Settings → Billing and Licensing → Usage this month**
> - View real-time consumption for each service
> - Download usage reports for detailed analysis
> 
> [Learn more about setting up budgets to control spendings](https://docs.github.com/en/billing/tutorials/set-up-budgets)
> 
> ## 5\. Canceling Subscriptions
> 
> ### Using the Virtual Assistant (GitHub Pro)
> 
> For quick cancellations:
> 
> 1. Visit [GitHub Support](https://support.github.com/contact-next?tags=hubberfy_billing_and_payments) ([https://support.github.com/contact-next](https://support.github.com/contact-next))
> 2. **Select An Account**
> 3. Continue
> 4. Follow the virtual assistant's guidance
> 5. Available 24/7 for instant help
> 
> **After cancellation:**
> 
> - You keep access until the end of your current billing period
> - No refund for unused time
> - You can re-subscribe anytime
> 
> Note  
> Cancelling subscriptions via the Virtual Assistant is only for Copilot Pro subscriptions and refunds are automatically issued in the VA.  
> Learn more: [Canceling your Copilot subscription](https://docs.github.com/en/copilot/how-tos/manage-your-account/view-and-change-your-copilot-plan)
> 
> ### Downgrading GitHub Pro/Team
> 
> **For Personal Accounts (GitHub Pro):**
> 
> 1. Go to **Settings → Billing and licensing**
> 2. Click **Edit** next to your plan
> 3. Select **Downgrade to Free**
> 4. Confirm downgrade
> 
> **For Organizations (Team):**
> 
> 1. Go to organization → **Settings → Billing and licensing**
> 2. Click **Edit** next to your plan
> 3. Select **Downgrade** or **Cancel**
> 4. Confirm (requires organization owner permissions)
> 
> **What you'll lose:**
> 
> - Advanced features (required reviewers, code owners, etc.)
> - Increased Actions minutes and storage
> - Private repositories may become public if over Free plan limits
> 
> Learn more: [Downgrading your GitHub subscription](https://docs.github.com/en/billing/how-tos/manage-plan-and-licenses/downgrade-plan)
> 
> ### Stopping Usage-Based Services
> 
> To stop charges for Codespaces, Actions, or Packages:  
> **Stop All Charges:**
> 
> 1. Go to **Settings → Billing and licensing → Budgets**
> 2. Find the service budget
> 3. Click **Delete budget** or set to **pause service at limit**
> 
> **For Codespaces Specifically:**
> 
> - Delete all active codespaces at [github.com/codespaces](https://github.com/codespaces)
> - Remove the Codespaces budget
> - Disable automatic creation in repository settings
> 
> ### Cancellation Timing and Refunds
> 
> Subscription Type When Access Ends Refund Policy  
> Copilot Pro End of billing period No  
> GitHub Pro Immediate downgrade Prorated credit may apply  
> Team End of billing period Contact sales  
> Usage-based services Immediately Charged only for actual usage  
> **Check your next billing date:** Go to **Settings → Billing and licensing → Overview** to see when your current period ends.
> 
> ### Pre-Cancellation Checklist
> 
> Before canceling, remember to:
> 
> - Backup important data (repositories, issues, discussions)
> - Review collaborator access impacts
> - Check private repository status
> - Download invoices for your records
> - Cancel related budgets and services
> - Note your renewal date
> 
> ## Frequently Asked Questions
> 
> ### General Billing Questions
> 
> ### Payment and Security
> 
> ### Budgets and Usage
> 
> ### Plan and Subscription Changes
> 
> ### Troubleshooting
> 
> ### Organization Billing
> 
> ### Support and Resources
> 
> ## Quick Reference: Preventing Common Billing Issues
> 
> Follow these best practices to avoid common problems:
> 
> 1. ✅ **Always subscribe via github.com in a web browser**
> 2. ✅ **Create budgets immediately** for any usage-based services (Codespaces, Actions, Packages)
> 3. ✅ **Match billing addresses exactly** to your bank records when updating payment info
> 4. ✅ **Understand plan differences** before subscribing (Pro ≠ Copilot)
> 5. ✅ **Use the virtual assistant** at [support.github.com](https://support.github.com/) for quick help
> 6. ✅ **Keep payment methods current** and set reminders before card expiration
> 7. ✅ **Enable billing email notifications** for payment failures and budget alerts
> 8. ✅ **Review billing settings monthly** to catch issues early
> 
> ## Additional Resources
> 
> **Official Documentation:**
> 
> - [GitHub Billing Documentation](https://docs.github.com/en/billing)
> - [GitHub Plans Overview](https://docs.github.com/en/get-started/learning-about-github/githubs-plans)
> 
> **Support:**
> 
> - [GitHub Support Portal](https://support.github.com/)
> - [GitHub Community Discussions](https://github.com/orgs/community/discussions/categories/general?discussions_q=is%3Aopen+category%3AGeneral+label%3Abilling)
> - [GitHub Status](https://www.githubstatus.com/)
> 
> **Copilot:**
> 
> - [Requests in GitHub Copilot](https://docs.github.com/en/copilot/concepts/billing/copilot-requests)
> - [About billing for individual GitHub Copilot plans](https://docs.github.com/en/copilot/concepts/billing/billing-for-individuals#about-premium-requests)
> 
> *This guide is community-maintained and based on common billing issues and questions. For the most up-to-date information, always refer to [GitHub's official documentation](https://docs.github.com/en/billing). Last updated Oct, 2025*

### This comment was marked as duplicate.

Show comment

Hide comment

#### Admin17k

> *คู่มือฉบับสมบูรณ์นี้จะช่วยคุณใช้งานระบบเรียกเก็บเงินของ GitHub แก้ไขปัญหาการชำระเงินทั่วไป และจัดการการสมัครรับข้อมูลของคุณได้อย่างมีประสิทธิภาพ ไม่ว่าคุณจะกำลังแก้ไขปัญหาการชำระเงินที่ถูกปฏิเสธ หรือกำลังพยายามทำความเข้าใจกับแพลตฟอร์มการเรียกเก็บเงินใหม่ คุณจะพบวิธีแก้ปัญหาแบบทีละขั้นตอนได้ที่นี่*
> 
> ## สารบัญ
> 
> 1. [ทำความเข้าใจแผนและการสมัครใช้งาน GitHub](#1-understanding-github-plans--subscriptions)
> 2. [วิธีการชำระเงินและการแก้ไขปัญหา](#2-payment-methods--troubleshooting)
> 3. [การจัดการข้อมูลการเรียกเก็บเงิน](#3-managing-billing-information)
> 4. [งบประมาณและการกำหนดค่าการใช้งาน](#4-budgets--usage-configuration)
> 5. [การยกเลิกการสมัครสมาชิก](#5-canceling-subscriptions)
> 6. [คำถามที่พบบ่อย](#6-frequently-asked-questions)
> 
> ## 1\. ทำความเข้าใจแผนและการสมัครใช้งาน GitHub
> 
> ### การเลือกแผนที่เหมาะสม
> 
> GitHub นำเสนอผลิตภัณฑ์สองประเภทที่แตกต่างกันซึ่งมีจุดประสงค์การใช้งานที่แตกต่างกัน:
> 
> **แผนแพลตฟอร์ม GitHub** (ฟรี, Pro, Team, Enterprise)
> 
> - คุณสมบัติการโฮสต์และการทำงานร่วมกันของที่เก็บข้อมูล
> - GitHub Actions คำนวณนาที
> - การจัดสรรแพ็กเกจและพื้นที่จัดเก็บ
> - เครื่องมือการรักษาความปลอดภัยและการปฏิบัติตามข้อกำหนดขั้นสูง
> 
> **แผน GitHub Copilot** (Pro, Pro+, Business, Enterprise)
> 
> - ข้อเสนอแนะโค้ดที่ขับเคลื่อนด้วย AI
> - การช่วยเหลือด้านแชทและโค้ดอินไลน์
> - การรวม IDE และ CLI
> - Copilot เป็นส่วนเสริม ไม่รวมอยู่ในแผนแพลตฟอร์ม
> 
> สำคัญ
> 
> สิ่งเหล่านี้เป็นการสมัครสมาชิกแยกต่างหาก GitHub Pro ไม่มี Copilot และ Copilot ไม่มีฟีเจอร์ของ GitHub Pro
> 
> ### คู่มือการตัดสินใจอย่างรวดเร็ว
> 
> เลือกแผนของคุณตามความต้องการของคุณ:
> 
> ความต้องการของคุณ แผนที่แนะนำ  
> นาทีการดำเนินการ ความร่วมมือขั้นสูง GitHub Pro ($4/เดือน)  
> ข้อเสนอแนะและความช่วยเหลือเกี่ยวกับโค้ด AI Copilot Pro ($10/เดือน)  
> ทั้งฟีเจอร์ของแพลตฟอร์มและความช่วยเหลือด้านการเขียนโค้ด AI GitHub Pro + Copilot Pro  
> การทำงานร่วมกันเป็นทีมด้วยการเขียนโค้ด AI ทีม GitHub + Copilot Business
> 
> ### การเปรียบเทียบคุณสมบัติ
> 
> คุณสมบัติ GitHub ฟรี GitHub โปร โคไพล็อต โปร  
> ที่เก็บข้อมูลสาธารณะและส่วนตัว ✅ ไม่จำกัด ✅ ไม่จำกัด ไม่มีข้อมูล  
> โค้ดสเปซ 120 ชั่วโมงหลักและพื้นที่เก็บข้อมูล 15GB/เดือน 180 ชั่วโมงหลักและพื้นที่เก็บข้อมูล 20GB/เดือน ไม่มีข้อมูล  
> การดำเนินการ นาที/เดือน 2,000 3,000 ไม่มีข้อมูล  
> การจัดเก็บพัสดุ 500 เมกะไบต์ 2GB ไม่มีข้อมูล  
> การตรวจสอบโค้ดขั้นสูง ❌ ✅ ไม่มีข้อมูล  
> การเติมโค้ด AI ❌ ❌ ✅  
> ความช่วยเหลือในการแชท ❌ ❌ ✅  
> หากต้องการเปรียบเทียบแบบสมบูรณ์ โปรดดู [เอกสารแผนอย่างเป็นทางการของ GitHub](https://docs.github.com/en/get-started/learning-about-github/githubs-plans) และ [การเรียกเก็บเงินสำหรับแผน GitHub Copilot แต่ละแผน](https://docs.github.com/en/copilot/concepts/billing/billing-for-individuals)
> 
> ### วิธีการสมัครสมาชิก
> 
> **สำหรับ GitHub Pro:**
> 
> 1. ไปที่ **การตั้งค่า → การเรียกเก็บเงินและใบอนุญาต**
> 2. คลิก **อัปเกรด** ภายใต้แผนปัจจุบันของคุณ
> 3. เลือก **GitHub Pro** และชำระเงินให้เสร็จสิ้น
> 4. เรียนรู้เพิ่มเติมที่นี่: [อัปเกรดแผน GitHub ของคุณ](https://docs.github.com/en/billing/how-tos/manage-plan-and-licenses/upgrade-plan)
> 
> **สำหรับ Copilot:**
> 
> 1. เยี่ยมชม [github.com/github-copilot/signup](https://github.com/github-copilot/signup)
> 2. เลือกระดับของคุณ (Pro, Business หรือ Enterprise)
> 3. ชำระเงินให้ครบถ้วนด้วยวิธีการชำระเงินที่ถูกต้อง
> 4. เรียนรู้เพิ่มเติม: [ทำความเข้าใจเกี่ยวกับใบอนุญาต Copilot](https://docs.github.com/en/billing/concepts/product-billing/github-copilot-licenses)
> 
> ## 2\. วิธีการชำระเงินและการแก้ไขปัญหา
> 
> ### วิธีการชำระเงินที่รองรับ
> 
> GitHub ยอมรับ:
> 
> - **บัตรเครดิต/เดบิต:** Visa, Mastercard, American Express, Discover
> - \*\*PayPal:\*\*มีให้บริการในบางภูมิภาค
> 
> **Best Practice:** Always subscribe through **github.com in a web browser** for the most reliable experience. Mobile app purchases or third-party payment processors may charge you without activating your subscription.
> 
> ### Card Declines and Failed Payments
> 
> #### Common Causes
> 
> - Insufficient funds or credit limit reached
> - Bank fraud protection blocking international transactions
> - Expired or incorrect card details
> - Billing address mismatch with bank records
> - Geographic restrictions on the card
> 
> #### Resolution Steps
> 
> 1. **Verify card details:** Double-check card number, expiration date, CVV, and billing address
> 2. **Contact your bank:**
> 	- Ask them to authorize charges from "GITHUB.COM"
> 		- Confirm international transactions are enabled (GitHub processes through US-based systems)
> 		- Check if they're blocking the transaction for fraud protection
> 3. **Try a different card:** If issues persist, use an alternative payment method
> 4. **Wait between attempts:** Allow 15-30 minutes between retries to avoid triggering additional fraud blocks
> 
> To update your payment method, go to **Settings → Billing and licensing → Payment information**. Learn more: [Managing your payment method](https://docs.github.com/en/billing/how-tos/set-up-payment/manage-payment-info?versionId=free-pro-team%40latest&productId=billing&restPage=concepts%2Cproduct-billing%2Cgithub-copilot-licenses)
> 
> ### Payment Processed But Subscription Not Active
> 
> This typically happens when using non-recommended payment channels:
> 
> **❌ High-Risk Methods:**
> 
> - Cryptocurrency wallets
> - Third-party payment processors
> 
> **✅ Recommended Method:**
> 
> - Subscribe via **github.com** in a web browser
> - Use credit/debit card or PayPal directly
> 
> #### If You're Already Charged
> 
> 1. Check subscription status: **Settings → Billing and licensing**
> 2. Wait 10 minutes for processing
> 3. If still inactive, **do not purchase again**
> 4. Contact [GitHub Support](https://support.github.com/) with your transaction receipt
> 5. Support will activate your plan or process a refund
> 
> Learn more: [Troubleshooting failed payments](https://docs.github.com/en/billing/how-tos/troubleshooting)
> 
> ### Authorization Holds Explained
> 
> When adding a payment method or starting a subscription, GitHub performs a temporary authorization check (typically $1-$133 USD depending on plan type). This verifies your card is valid.
> 
> **Key Facts:**
> 
> - ✅ This is not a real charge—it's a temporary hold
> - ✅ The hold automatically releases within 5-7 business days
> - ✅ Your actual subscription charge posts separately
> - ❌ If authorization fails, your account may be temporarily locked
> 
> #### If Authorization Fails
> 
> 1. Contact your bank to understand why the authorization was declined
> 2. Ensure sufficient available credit for the hold amount
> 3. Verify billing address matches your bank's records exactly
> 4. Once resolved, contact [GitHub Support](https://support.github.com/) to unlock your account
> 
> ## 3\. Managing Billing Information
> 
> ### Updating Your Billing Address
> 
> #### For Personal Accounts
> 
> 1. Go to **Settings → Billing and licensing**
> 2. Click **Payment information**
> 3. Update your name and address fields
> 4. Click **Save billing information**
> 
> #### For Organizations
> 
> 1. Navigate to your organization page
> 2. Go to **Settings → Billing and licensing**
> 3. Click **Edit** under **Payment information**
> 4. Update the name and address (you must be an organization owner)
> 5. Save changes
> 
> Learn more: [Adding or editing a payment method](https://docs.github.com/en/billing/managing-your-github-billing-settings/adding-or-editing-a-payment-method)
> 
> ### Troubleshooting Update Issues
> 
> If you can't save billing information changes, try these solutions:
> 
> #### Common Problems and Fixes
> 
> **1\. Field Validation Errors**
> 
> Error Message Cause Solution  
> "Invalid billing address" Address doesn't match bank records Contact your bank for exact address format, then match it precisely  
> "City not recognized" Misspelling or unsupported characters Double-check spelling; use standard English characters only  
> "Postal code invalid" Wrong format for your country Verify format (US: 12345 or 12345-6789)  
> "Payment method update failed" General processing error Wait 10 minutes and retry  
> **2\. Address Entry Best Practices**
> 
> - ✅ Match your bank records exactly (including abbreviations)
> - ✅ Avoid special characters (é, ñ, ü, ™, ®, emojis)
> - ✅ Use standard abbreviations (St, Ave, Apt, CA, NY)
> - ✅ Double-check city spelling (Pittsburgh not Pittsburg)
> 
> **3\. Browser Issues**
> 
> Try these troubleshooting steps:
> 
> 1. **Clear cache or use incognito mode:**
> 	- Open a private/incognito browsing window
> 		- Navigate to billing settings
> 		- Attempt the update again
> 2. **Try a different browser:**
> 	- Switch between Chrome, Firefox, Safari, or Edge
> 		- Temporarily disable browser extensions
> 3. **Use keyboard navigation:**
> 	- Tab through fields instead of clicking
> 		- Press Enter after the last field
> 
> ### Removing or Changing Payment Methods
> 
> You cannot remove a payment method if you have:
> 
> - Active paid subscriptions
> - Unpaid invoices or balances
> - Active budgets for usage-based services
> 
> #### How to Remove a Payment Method
> 
> 1. Add a new payment method first
> 2. Set the new method as **default**
> 3. Then remove the old payment method
> 
> Alternatively, cancel all paid subscriptions first, wait until the end of your billing cycle, then remove the payment method.
> 
> ### When to Contact Support
> 
> Reach out to [GitHub Support](https://support.github.com/) if:
> 
> - You've tried all troubleshooting steps without success
> - Your account is locked due to billing issues
> - You need to update billing details but don't have access to the payment method owner
> - You need help with complex organization billing
> 
> ## 4\. Budgets & Usage Configuration
> 
> ### Understanding the New Billing Platform
> 
> GitHub transitioned from **spending limits** to **budgets**, introducing important changes:
> 
> **Old System (Spending Limits):**
> 
> - Single setting for all services
> - Hard cap; service stopped when limit reached
> 
> **New System (Budgets):**
> 
> - Separate budget per service (Codespaces, Actions, Packages, LFS)
> - Email alerts at 75%, 100%, and 125% of budget
> - You choose: pause service or allow overages
> - Must be explicitly configured even if you had spending limits before
> 
> Learn more: [About the new billing platform](https://docs.github.com/en/rest/billing/billing?apiVersion=2022-11-28#about-billing)
> 
> ### Why Your Codespaces or Actions Stopped Working
> 
> After the billing platform migration, usage-based services require explicit budgets before they'll work, even if you previously had spending limits configured.
> 
> **Common symptoms:**
> 
> - Codespaces won't start or show as disabled
> - Actions workflows fail with billing errors
> - Services inaccessible despite having a payment method on file
> 
> ### Creating a Budget
> 
> #### For Personal Accounts
> 
> 1. Go to **Settings → Billing and licensing**
> 2. Scroll to **Budgets and alerts** section
> 3. Click **New budget**
> 4. Select the service (Codespaces, Actions, Packages, or LFS)
> 5. Set your monthly budget amount (minimum $1)
> 6. Choose behavior when budget is reached:
> 	- **Pause service** (recommended to prevent overspending)
> 		- **Allow overage** (service continues; you'll be charged for additional usage)
> 7. Click **Create budget**
> 
> #### For Organizations
> 
> 1. Navigate to organization → **Settings → Billing and licensing**
> 2. Go to **Budgets and alerts**
> 3. Follow steps 3-7 above
> 
> **Important:** Each service requires its own budget. If you use both Codespaces and Actions, create separate budgets for each.
> 
> Learn more: [Creating and editing budgets](https://docs.github.com/en/billing/tutorials/set-up-budgets?apiVersion=2022-11-28&versionId=free-pro-team%40latest&category=billing&subcategory=billing)
> 
> ### Budget Troubleshooting
> 
> #### Budget Not Saving or Applying
> 
> **Troubleshooting checklist:**
> 
> 1. ✅ **Verify payment method:** Go to **Settings → Billing and licensing → Payment information** and ensure a valid payment method is active
> 2. ✅ **Check minimum amount:** Budget must be at least $1 USD
> 3. ✅ **Confirm service selection:** Each budget applies to only one service
> 4. ✅ **Wait for activation:** Budgets can take 2-5 minutes to activate
> 5. ✅ **Clear cache:** Try incognito mode or a different browser
> 
> If the budget doesn't appear after 10 minutes, contact [GitHub Support](https://support.github.com/) with the service name, budget amount, and any error messages.
> 
> ### Understanding Budget Mechanics
> 
> Feature Details  
> **Scope** Per service (one budget each for Codespaces, Actions, Packages, LFS)  
> **Period** Monthly (resets on billing cycle date)  
> **Alerts** Email notifications at 75%, 100%, and 125% of budget  
> **Charges** You're only charged for actual usage, not the budget amount  
> **Example:** Setting a $50 budget doesn't mean you'll be charged $50. It's a spending limit, not a subscription fee. If you only use $20 worth of services, you only pay $20.
> 
> ### Monitoring Usage
> 
> Check current usage against your budget:
> 
> - Go to **Settings → Billing and Licensing → Usage this month**
> - View real-time consumption for each service
> - Download usage reports for detailed analysis
> 
> [Learn more about setting up budgets to control spendings](https://docs.github.com/en/billing/tutorials/set-up-budgets)
> 
> ## 5\. Canceling Subscriptions
> 
> ### Using the Virtual Assistant (GitHub Pro)
> 
> For quick cancellations:
> 
> 1. Visit [GitHub Support](https://support.github.com/contact-next?tags=hubberfy_billing_and_payments) ([https://support.github.com/contact-next](https://support.github.com/contact-next))
> 2. **Select An Account**
> 3. Continue
> 4. Follow the virtual assistant's guidance
> 5. Available 24/7 for instant help
> 
> **After cancellation:**
> 
> - You keep access until the end of your current billing period
> - No refund for unused time
> - You can re-subscribe anytime
> 
> Note
> 
> Cancelling subscriptions via the Virtual Assistant is only for Copilot Pro subscriptions and refunds are automatically issued in the VA.
> 
> Learn more: [Canceling your Copilot subscription](https://docs.github.com/en/copilot/how-tos/manage-your-account/view-and-change-your-copilot-plan)
> 
> ### Downgrading GitHub Pro/Team
> 
> **For Personal Accounts (GitHub Pro):**
> 
> 1. Go to **Settings → Billing and licensing**
> 2. Click **Edit** next to your plan
> 3. Select **Downgrade to Free**
> 4. Confirm downgrade
> 
> **For Organizations (Team):**
> 
> 1. Go to organization → **Settings → Billing and licensing**
> 2. Click **Edit** next to your plan
> 3. Select **Downgrade** or **Cancel**
> 4. Confirm (requires organization owner permissions)
> 
> **What you'll lose:**
> 
> - Advanced features (required reviewers, code owners, etc.)
> - Increased Actions minutes and storage
> - Private repositories may become public if over Free plan limits
> 
> Learn more: [Downgrading your GitHub subscription](https://docs.github.com/en/billing/how-tos/manage-plan-and-licenses/downgrade-plan)
> 
> ### Stopping Usage-Based Services
> 
> To stop charges for Codespaces, Actions, or Packages:
> 
> **Stop All Charges:**
> 
> 1. Go to **Settings → Billing and licensing → Budgets**
> 2. Find the service budget
> 3. Click **Delete budget** or set to **pause service at limit**
> 
> **For Codespaces Specifically:**
> 
> - Delete all active codespaces at [github.com/codespaces](https://github.com/codespaces)
> - Remove the Codespaces budget
> - Disable automatic creation in repository settings
> 
> ### Cancellation Timing and Refunds
> 
> Subscription Type When Access Ends Refund Policy  
> Copilot Pro End of billing period No  
> GitHub Pro Immediate downgrade Prorated credit may apply  
> Team End of billing period Contact sales  
> Usage-based services Immediately Charged only for actual usage  
> **Check your next billing date:** Go to **Settings → Billing and licensing → Overview** to see when your current period ends.
> 
> ### Pre-Cancellation Checklist
> 
> Before canceling, remember to:
> 
> - Backup important data (repositories, issues, discussions)
> - Review collaborator access impacts
> - Check private repository status
> - Download invoices for your records
> - Cancel related budgets and services
> - Note your renewal date
> 
> ## Frequently Asked Questions
> 
> ### General Billing Questions
> 
> ### Payment and Security
> 
> ### Budgets and Usage
> 
> ### Plan and Subscription Changes
> 
> ### Troubleshooting
> 
> ### Organization Billing
> 
> ### Support and Resources
> 
> ## Quick Reference: Preventing Common Billing Issues
> 
> Follow these best practices to avoid common problems:
> 
> 1. ✅ **Always subscribe via github.com in a web browser**
> 2. ✅ **Create budgets immediately** for any usage-based services (Codespaces, Actions, Packages)
> 3. ✅ **Match billing addresses exactly** to your bank records when updating payment info
> 4. ✅ **Understand plan differences** before subscribing (Pro ≠ Copilot)
> 5. ✅ **Use the virtual assistant** at [support.github.com](https://support.github.com/) for quick help
> 6. ✅ **Keep payment methods current** and set reminders before card expiration
> 7. ✅ **Enable billing email notifications** for payment failures and budget alerts
> 8. ✅ **Review billing settings monthly** to catch issues early
> 
> ## Additional Resources
> 
> **Official Documentation:**
> 
> - [GitHub Billing Documentation](https://docs.github.com/en/billing)
> - [GitHub Plans Overview](https://docs.github.com/en/get-started/learning-about-github/githubs-plans)
> 
> **Support:**
> 
> - [GitHub Support Portal](https://support.github.com/)
> - [GitHub Community Discussions](https://github.com/orgs/community/discussions/categories/general?discussions_q=is%3Aopen+category%3AGeneral+label%3Abilling)
> - [GitHub Status](https://www.githubstatus.com/)
> 
> **Copilot:**
> 
> - [Requests in GitHub Copilot](https://docs.github.com/en/copilot/concepts/billing/copilot-requests)
> - [About billing for individual GitHub Copilot plans](https://docs.github.com/en/copilot/concepts/billing/billing-for-individuals#about-premium-requests)
> 
> *This guide is community-maintained and based on common billing issues and questions. For the most up-to-date information, always refer to [GitHub's official documentation](https://docs.github.com/en/billing). Last updated Oct, 2025*

### gravouilj on Dec 28, 2025

I've been stucked with this message for weeks now "We may place a temporary hold on your payment method to verify its validity. This is not a charge, and it will be released automatically after verification." I've tried everything possible (different browser, emptying cache etc), paying with paypal, credit/debit card, I can't figure out how to simply subscribe to copilot pro, it is so frustrating. On top I get no answers from the support....

0 replies

### sophiasmithastri on Feb 10

Thanks for putting this together billing questions come up constantly and this guide covers the common why was I charged but nothing changed situations really well. It might help to add a quick note up top that Pro and Copilot are separate subscriptions, since that mix up seems to drive a lot of the confusion.

0 replies

### This comment was marked as off-topic.

Show comment

Hide comment

#### reoxc

Helllo

### sajadThapa04 on Mar 22

1 reply

#### Zaidux on Mar 23

A big most likely.

### Bayarjargalaa on Apr 5

I have paid for a full year and still can't activate my license. Where should I go?

1 reply

Hi [@Bayarjargalaa](https://github.com/Bayarjargalaa)

Thanks for reaching out. You can find solutions to most billing issues in our [💳 GitHub Community Discussions Billing & Subscription Guide](https://github.com/orgs/community/discussions/178128).

If you need more help, the best place to get answers is by opening a ticket on our [Support page](https://support.github.com/contact).

Best of luck!

edited

### Personuo on Apr 10

HI ，I needd you help, It seems I may have triggered a bug in your refund system.

[https://support.github.com/ticket/4267333](https://github.com/orgs/community/discussions/url)

Refund request for Copilot Pro annual subscription (Billing and payments)

Please describe your Copilot billing, signup, or activation issue  
Hi,

I was a GitHub Copilot Pro annual subscriber ($100/year).

On the same day my annual subscription renewed, I upgraded to Copilot Pro+ to try it out. However, I noticed that the system converted my plan into a monthly subscription and I lost my annual plan discount.

I then reverted back to Copilot Pro, but my annual subscription was no longer available, and I was switched to a monthly plan instead.

It seems that my annual subscription was effectively canceled, but I did not receive any refund. Since I only used it for a very short time, I would like to request a prorated refund (around $90).

This appears to be an unintended upgrade/downgrade flow, and I would really appreciate your help in resolving it.

My Transaction ID ch\_3TGLpwJFr6CCHwIi0oAjko9s

Thank you.

[![image](https://private-user-images.githubusercontent.com/8104770/576740895-511c9cd5-c822-46a8-a153-58c7a67e542d.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODM1NDkxODUsIm5iZiI6MTc4MzU0ODg4NSwicGF0aCI6Ii84MTA0NzcwLzU3Njc0MDg5NS01MTFjOWNkNS1jODIyLTQ2YTgtYTE1My01OGM3YTY3ZTU0MmQucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDcwOCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA3MDhUMjIxNDQ1WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9YzU4NDY3Yzk4MzQ2Y2JhZTJjZWRjMjMyMmRlZGFmMTZhMDQxNzdiODg5NTQ4YTQ0NGQyYjQzMWE0MTI1YjFiNiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.5tKHfcTUxzCBoJbs1wuiP_zDP9OP97ooIGlNwd1rjSs)](https://private-user-images.githubusercontent.com/8104770/576740895-511c9cd5-c822-46a8-a153-58c7a67e542d.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODM1NDkxODUsIm5iZiI6MTc4MzU0ODg4NSwicGF0aCI6Ii84MTA0NzcwLzU3Njc0MDg5NS01MTFjOWNkNS1jODIyLTQ2YTgtYTE1My01OGM3YTY3ZTU0MmQucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDcwOCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA3MDhUMjIxNDQ1WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9YzU4NDY3Yzk4MzQ2Y2JhZTJjZWRjMjMyMmRlZGFmMTZhMDQxNzdiODg5NTQ4YTQ0NGQyYjQzMWE0MTI1YjFiNiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.5tKHfcTUxzCBoJbs1wuiP_zDP9OP97ooIGlNwd1rjSs)

I paid for the annual renewal on March 29, but it has been two weeks and I still haven’t received a refund. I’ve already tried the refund bot, and I also submitted a support ticket at the time. Back then, I wanted to revert to the Copilot Pro annual plan, but no one responded. I then closed that ticket and submitted a new one requesting a prorated refund of $90, since I am now on the Copilot Pro monthly plan and have already used it for about half a month.

old support ticket [https://support.github.com/ticket/4219842](https://github.com/orgs/community/discussions/url)

1 reply

#### Personuo on Apr 10

And, That after I upgraded to Pro+ and then downgraded back to Pro, the system did not charge me any additional fees.  
So, out of the $100 I paid, after deducting $10 for this month, I should receive a $90 refund.

My tokens dissapeared in 2 days. before i could use them for a month!!?? what happened. Doing the same work on VS code, and same ai.

0 replies

Remember, contributions to this repository should follow its [code of conduct](https://github.com/community/community/blob/dd77c447350df6ffd0e1c2752405fa8cab2b396f/CODE_OF_CONDUCT.md).