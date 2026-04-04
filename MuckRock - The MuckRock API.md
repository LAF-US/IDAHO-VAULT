---
source: "https://www.muckrock.com/api/"
author:
  - "MuckRock"
published:
created: 2026-03-30
---
![](https://d3gn0r3afghep.cloudfront.net/news_photos/2016/06/03/api.jpg)

## The MuckRock API

The MuckRock API, or application programming interface, provides a way to access MuckRock data programmatically. This guide will give you what you need to get up and running. The API is accessible through HTTPS and our Python library, [python-muckrock](https://python-muckrock.readthedocs.io/en/latest/) . We recommend our library for scripts, automations, and notebooks—it provides a convenient helper for authenticating with your MuckRock account, searching the database and filing records requests.

## Documentation

The MuckRock API has a [built-in internal referential schema](https://www.muckrock.com/api_v2/schema/redoc/) that lists all parameters for different endpoints and operations. We also encourage users to read through our Python library's [getting started section](https://python-muckrock.readthedocs.io/en/latest/gettingstarted.html) for concrete examples of a workflow.  

## Rate Limiting

The API (and generally, the entire site) is rate limited to one request per second, however you can burst these requests up to 20 per second for as long as the average runs less than 1 per second over a 20 second period.

## Endpoints

The current API endpoint is [`https://www.muckrock.com/api_v2/`](https://www.muckrock.com/api_v2/). It is accessible without any authentication. Making a query against this top-level address will provide a list of available objects and their endpoints. The current list of available objects includes:

- requests
- communications
- files
- agencies
- jurisdictions
- users
- organizations
- projects

## Authentication

Some endpoint operations are accessible without providing any authentication. Others, like filing a request, require authentication. If you're ever unsure, if an operation requires authentication and you aren't authenticated you'll receive a response: "Authentication credentials were not provided". Authentication is done using MuckRock Accounts access tokens. To retrieve your first access token, you must authenticate using username and password with a POST to the following endpoint: [`https://accounts.muckrock.com/api/token/`](https://accounts.muckrock.com/api/token/)

Authenticating with this endpoint you will receive a response that includes an access and refresh token. The access token is valid for 5 minutes after which it will stop working. To continue making API requests, you will need to POST the refresh token you received earlier to the following endpoint to be issued an updated access and refresh token: [`https://accounts.muckrock.com/api/refresh/`](https://accounts.muckrock.com/api/refresh/)

Using our Python wrapper for the MuckRock API, [python-muckrock](https://python-muckrock.readthedocs.io/en/latest/) , handles all of the authentication requirements for you behind the scenes so that you don't have to manage tokens yourself.

## Pagination

Our responses are paginated, with a default of 50 items per page. The number of results per page can be changed by providing a `page_size` query argument.

## Response Formats

By default, requests to endpoints will return an HTML “explorer” view that is very easy to use in a browser, but not-so-much in code. To get JSON-formatted responses, either include the `application/json` value to the `content-type` header or include the `format=json` query argument.

## Submitting Requests

FOIA Requests can be filed through our API. This can be done by sending an authenticated `POST` request to the `/requests/` endpoint. The following parameters are available:

`agencies` (Array of ints) \*Required

List of agency IDs of agencies you would like to send this request to.

`embargo_status` (String)

The embargo status for the request (e.g., public, embargo, permanent). Embargo embargoes the request until 30 days after the request has been marked complete while permanent will permanently embargo the request. Regular embargoes are only available to paid professional users and permanent embargoes are only available to paid organizational members.

`title` (String) \*Required

The title of the request

`requested_docs` (String) \*Required

Description of the documents being requested. This will be inserted into the default form language for a request.

`organization` (int)

ID of the organization submitting this request. Must be an organization you belong to.

Filing a request through the API will subtract from your account’s available FOIA request count. If no requests have been purchased, the request will be saved as a draft but not sent. After purchasing more requests from your account page, the draft request can be filed manually. Filing a request without any purchased requests will return a HTTP 402 error.

## Examples

The [documentation for our Python library](https://python-muckrock.readthedocs.io/en/latest/gettingstarted.html) for the MuckRock API includes examples on interacting with many of our endpoints. We also provide [an example script](https://github.com/MuckRock/API-examples/blob/master/upload_responsive_documents_to_documentcloud.py) that incorporates both the MuckRock and DocumentCloud APIs as well as a [DocumentCloud Add-On](https://github.com/duckduckgrayduck/request-downloader/blob/main/main.py) that uses both APIs.