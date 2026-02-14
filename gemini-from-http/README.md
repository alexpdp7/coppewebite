# Gemini from http

`proxy.py` is a Gemini server that proxies all content to an http or https server.

`proxy.py` loads certificates following the structure of Apache mod_md.

## Providing the certificates via systemd credentials

With `/etc/systemd/system/gemini-from-http.service`:

```
[Service]
LoadCredential=certificates:/etc/apache2/md/domains/
ExecStart=.../proxy.py --certificates-from-credential certificates
DynamicUser=true
CapabilityBoundingSet=
PrivateDevices=true
ProtectClock=true
ProtectKernelLogs=true
ProtectControlGroups=true
ProtectKernelModules=true
SystemCallArchitectures=native
MemoryDenyWriteExecute=true
RestrictNamespaces=true
ProtectHostname=true
LockPersonality=true
ProtectKernelTunables=true
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
RestrictRealtime=true
# If you don't put proxy.py in a home directory... ProtectHome=true
ProtectProc=invisible
ProcSubset=pid
PrivateUsers=self
SystemCallFilter=@system-service
SystemCallErrorNumber=EPERM
UMask=7777
```

Systemd injects the certificates to a private path than only `proxy.py` can read.
The injection is a one off, so you must restart the service to get updated certificates.

## Providing the certificates manually

To run `proxy.py` as a regular user, you can run the `package-mod-md-certs` script as root to copy the certificates to your user:

```
su -c ./package-mod-md-certs | tar x
```

Then you can run:

```
./proxy.py --certificates-from-path domains/
```
