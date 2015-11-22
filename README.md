# IPAUTH-API

IPAUTH-API is a tool to help in the SSH access control. How it works:

  - Creates a sqlite data base with user details (username, key, skey, old IP and current IP)
  - Users must be in the local system
  - Uses iptables to control the firewall access for the SSH port

Installation:

Create IPtables chain IPAUTH-API
```sh
# iptables -A IPAUTH-API -j reject
```

Redirect SSH traffic to IPAUTH-API chain:
```sh
# iptables -A IPAUTH-API -j reject
```


> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible. The idea is that a
> Markdown-formatted document should be
> publishable as-is, as plain text, without
> looking like it's been marked up with tags
> or formatting instructions.

This text you see here is *actually* written in Markdown! To get a feel for Markdown's syntax, type some text into the left window and watch the results in the right.

### Version
3.2.0

### Tech

Dillinger uses a number of open source projects to work properly:

* [AngularJS] - HTML enhanced for web apps!
* [Ace Editor] - awesome web-based text editor
* [Marked] - a super fast port of Markdown to JavaScript
* [Twitter Bootstrap] - great UI boilerplate for modern web apps
* [node.js] - evented I/O for the backend
* [Express] - fast node.js network app framework [@tjholowaychuk]
* [Gulp] - the streaming build system
* [keymaster.js] - awesome keyboard handler lib by [@thomasfuchs]
* [jQuery] - duh

And of course Dillinger itself is open source with a [public repository][dill]
 on GitHub.

### Installation
