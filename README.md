Simple CLI app that generates tokens compatible with Google Authenticator. I implemented this mainly to understand how it works, you should probably not use this.

Example output:

```sh
$ go run main.go "<your key>"
934523 (17 second(s) remaining)
```

Relevant RFCs:

* http://tools.ietf.org/html/rfc4226
* http://tools.ietf.org/html/rfc6238
