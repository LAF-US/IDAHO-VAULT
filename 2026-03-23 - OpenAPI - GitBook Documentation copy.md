---
source: "https://gitbook.com/docs/api-references/openapi"
author:
published: 2026-03-23
created: 2026-04-23
---
Manually writing REST API documentation can be a time-consuming process. Fortunately, GitBook streamlines this task by allowing you to import OpenAPI documents, which detail your API’s structure and functionality.

The OpenAPI Specification (OAS) is a framework that developers use to document REST APIs. Written in JSON or YAML, it outlines all your endpoints, parameters, schemas, and authentication schemes.

Once imported into GitBook, these documents are transformed into interactive and testable API blocks that visually represent your API methods—whether the specification is provided as a file or loaded from a URL.

GitBook supports [Swagger 2.0](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md) or [OpenAPI 3.0](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md) compliant files.

### Add a new pet to the store.

post

Add a new pet to the store.

Authorizations

OAuth2implicitRequired

Authorization URL:

Body

idinteger · int64OptionalExample: `10`

namestringRequiredExample: `doggie`

photoUrlsstring\[\]Required

statusstring · enumOptional

pet status in the store

Possible values:

Responses

post

/pet

```
POST /api/v3/pet HTTP/1.1
Authorization: Bearer YOUR_OAUTH2_TOKEN
Content-Type: application/json
Accept: */*
Content-Length: 133

{
  "id": 10,
  "name": "doggie",
  "category": {
    "id": 1,
    "name": "Dogs"
  },
  "photoUrls": [
    "text"
  ],
  "tags": [
    {
      "id": 1,
      "name": "text"
    }
  ],
  "status": "available"
}
```

```
{
  "id": 10,
  "name": "doggie",
  "category": {
    "id": 1,
    "name": "Dogs"
  },
  "photoUrls": [
    "text"
  ],
  "tags": [
    {
      "id": 1,
      "name": "text"
    }
  ],
  "status": "available"
}
```

### Test it (powered by Scalar)

GitBook's OpenAPI block also supports a "test it" functionality, which allows your users to test your API methods with data and parameters filled in from the editor.

Powered by [Scalar](https://scalar.com/), you won't need to leave the docs to see your API methods in action. See an example of this above.

#### FAQ

Last updated