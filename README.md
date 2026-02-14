# Coppewebite

Coppewebite is a project exploring interactions between the [Gemini protocol](https://geminiprotocol.net/) and the web.

* [`gemini-to-web`](gemini-to-web): Python library and command-line tools to convert Gemini to web formats.
* [`apache-configuration`](apache-configuration.md): documentation for configuring Apache httpd to make serve Gemtext as an alternative negotiated content type.
* [`gemini-from-http`](gemini-from-http): a Gemini proxy server that proxies all content to an http or https server.

`gemini-from-http` is particularly useful paired with an Apache httpd server configured to serve Gemtext as an alternative negotiated content type.
