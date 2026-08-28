# PKI / TLS Troubleshooting Guide

## 1. Confirm Basic Connectivity

Before assuming the certificate is the problem, verify that the service is reachable.

Examples:

```bash
curl -v https://target.example.com
```

or:

```bash
openssl s_client -connect target.example.com:443 -servername target.example.com
```

If the connection cannot be established at all, investigate DNS, routing, firewall rules, ports, or service availability before focusing on PKI.

## 2. Inspect the Server Certificate

Use OpenSSL to inspect the certificate presented by the server:

```bash
openssl s_client -connect target.example.com:443 -servername target.example.com
```

Important fields include:

- Subject
- Issuer
- Validity dates
- Certificate chain
- TLS protocol
- Negotiated cipher
- Verification result

A successful connection should normally include:

```text
Verification: OK
Verify return code: 0 (ok)
```

---

## 3. Check Certificate Trust

A certificate may be technically valid but still fail because the client does not trust the issuing CA.

Example failure:

```text
error 20 at 0 depth lookup: unable to get local issuer certificate
```

In the lab, verification failed when the custom root CA was not supplied:

```bash
openssl verify certs/server.crt
```

Verification succeeded when the trusted root was explicitly provided:

```bash
openssl verify \
  -CAfile certs/rootCA.crt \
  certs/server.crt
```

### Troubleshooting Conclusion

If the certificate validates when the correct CA is supplied, the problem is likely client trust configuration rather than a defective server certificate.

---

## 4. Check Hostname Validation

The hostname requested by the client must match a valid identity in the certificate.

In the lab, the client connected to:

```text
localhost
```

while the certificate identity was:

```text
internal.securitylab.local
```

This produced:

```text
SSL: certificate subject name 'internal.securitylab.local' does not match target host name 'localhost'
```

The issue was resolved by connecting with the correct hostname while mapping it to the local test server:

```bash
curl \
  --cacert certs/rootCA.crt \
  --resolve internal.securitylab.local:8443:127.0.0.1 \
  https://internal.securitylab.local:8443
```

### Troubleshooting Conclusion

A trusted certificate can still be rejected if the requested hostname does not match the certificate identity.

---

## 5. Check Subject Alternative Names

Modern TLS clients use the Subject Alternative Name (SAN) extension for hostname validation.

Inspect SAN values with:

```bash
openssl x509 \
  -in certs/server.crt \
  -noout \
  -text
```

The corrected lab certificate includes:

```text
X509v3 Subject Alternative Name:
    DNS:internal.securitylab.local
```

It also includes:

```text
X509v3 Extended Key Usage:
    TLS Web Server Authentication
```

### Troubleshooting Conclusion

A certificate should contain the required hostname in the SAN extension and should be valid for the intended usage.

---

## 6. Check Certificate Expiration

Inspect validity dates:

```bash
openssl x509 \
  -in certs/server.crt \
  -noout \
  -dates
```

The expired lab certificate produced:

```text
error 10 at 0 depth lookup: certificate has expired
```

### Troubleshooting Conclusion

Always check both `notBefore` and `notAfter`. A certificate may fail because it is expired or not yet valid.

---

## 7. Check the Certificate Chain

A server certificate may chain through an intermediate CA before reaching the trusted root.

Example:

```text
Server Certificate
      |
      v
Intermediate CA
      |
      v
Root CA
```

In the lab, verification failed when the intermediate CA was missing:

```text
error 20 at 0 depth lookup: unable to get local issuer certificate
```

Verification succeeded when the intermediate certificate was supplied:

```bash
openssl verify \
  -CAfile certs/rootCA.crt \
  -untrusted certs/intermediateCA.crt \
  certs/chain-server.crt
```

### Troubleshooting Conclusion

If the root CA is trusted but verification still fails, inspect whether the required intermediate certificates are being presented.

---

## 8. Check TLS Protocol Compatibility

TLS negotiation can fail before certificate validation if the client and server do not support a common protocol version.

In the lab:

```text
Server: TLS 1.2 only
Client: TLS 1.3 only
```

The result was:

```text
tlsv1 alert protocol version
Cipher is (NONE)
```

Connecting with TLS 1.2 succeeded:

```text
Protocol: TLSv1.2
Verify return code: 0 (ok)
```

### Troubleshooting Conclusion

A handshake failure may be caused by incompatible protocol versions rather than the certificate itself.

---

## 9. Check Cipher Compatibility

Even when the client and server agree on the TLS version, the handshake can fail if they do not share a compatible cipher suite.

In the lab, the server allowed:

```text
ECDHE-RSA-AES256-GCM-SHA384
```

while the client offered:

```text
ECDHE-RSA-AES128-GCM-SHA256
```

The handshake failed:

```text
ssl/tls alert handshake failure
Cipher is (NONE)
```

Using the matching cipher succeeded:

```text
New, TLSv1.2, Cipher is ECDHE-RSA-AES256-GCM-SHA384
```

### Troubleshooting Conclusion

If TLS versions match but the handshake still fails, inspect the cipher suites supported by both sides.

---

## 10. Troubleshooting Decision Flow

```text
Can the service be reached?
        |
        +-- No --> Check DNS, routing, firewall, port, service
        |
        v
Does the certificate chain validate?
        |
        +-- No --> Check root trust and intermediate certificates
        |
        v
Is the certificate within its validity period?
        |
        +-- No --> Renew or replace certificate
        |
        v
Does the hostname match the SAN?
        |
        +-- No --> Correct certificate identity or requested hostname
        |
        v
Do client and server support a common TLS version?
        |
        +-- No --> Correct protocol configuration
        |
        v
Do client and server support a common cipher?
        |
        +-- No --> Correct cipher configuration
        |
        v
TLS connection succeeds
```

## Evidence

Supporting command output is available in the [`evidence/`](evidence/) directory.
