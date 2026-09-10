# Linux Detection Opportunities

## 1. Repeated SSH Failures Followed by Success

### Detection Logic

Alert when:

- Multiple SSH authentication failures originate from the same source IP
- A successful login from that IP follows within a short time window

### Relevant Patterns

```text
Failed password
Accepted password
