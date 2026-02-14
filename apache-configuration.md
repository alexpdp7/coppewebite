# Apache configuration

With the following modules loaded in Apache httpd:

```
LoadModule negotiation_module /usr/lib/apache2/modules/mod_negotiation.so
LoadModule mime_module /usr/lib/apache2/modules/mod_mime.so
```

And the default mime types configuration:

```
TypesConfig /etc/mime.types
```

Then you can use the following configuration to make httpd serve Gemtext as an alternative negotiated content type:

```
# Associate the .gmi extension with text/gemini.
# This makes MultiViews consider .gmi files as an additional content type to negotiate for clients that request it.
AddType text/gemini .gmi

# Enable MultiViews so requests for /.../foo are content negotiated and can return either foo.html or foo.gmi.
<Directory ...>
	   Options MultiViews
</Directory>

# Change the DirectoryIndex to index so that MultiViews are used for indexes too.
DirectoryIndex index
```

With this configuration:

* `/` serves `index.html` or `index.gmi`.
* `/foo` serves `foo.html` or `foo.gmi`.
* `/foo/` serves `foo/index.html` or `foo/index.gmi`.

Interestingly, when there is no Accept header or when multiple matching types are present, http defaults to serving the smallest file.
In general, this means that httpd serves smaller gemtext files over HTML.
For example, when using `curl`, httpd serves gemtext, which is more readable than HTML on a terminal.

## Running Apache httpd as a regular user

On Debian, you can install Apache httpd by running the following commands:

```sh
sudo apt install apache2
sudo systemctl disable --now apache2  # Debian enables apache2 to start automatically when your system starts, disable the service to prevent this.
```

Then, if you create an `apache2.conf` in a directory with the following content:

```
LoadModule mpm_event_module /usr/lib/apache2/modules/mod_mpm_event.so
Listen 8000
PidFile logs/pid
ServerRoot .
DocumentRoot document_root
LoadModule authn_core_module /usr/lib/apache2/modules/mod_authn_core.so
LoadModule authz_core_module /usr/lib/apache2/modules/mod_authz_core.so
```

Then running the following command starts Apache httpd listening on port 8000:

```sh
/usr/sbin/apache2 -D FOREGROUND -d .
```
