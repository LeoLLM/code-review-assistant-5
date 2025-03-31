# Security-Related Code Review Template

## Input Validation
- [ ] All user inputs are validated
- [ ] Input validation occurs on server-side
- [ ] Input is sanitized before processing
- [ ] SQL injection protections in place

## Authentication & Authorization
- [ ] Authentication is properly implemented
- [ ] Authorization checks are in place
- [ ] Roles and permissions are correctly applied
- [ ] No hidden admin paths/backdoors

## Data Protection
- [ ] Sensitive data is encrypted in transit
- [ ] Sensitive data is encrypted at rest
- [ ] No hardcoded credentials/secrets
- [ ] Environment variables used for sensitive data
- [ ] No sensitive data in logs

## Session Management
- [ ] Sessions are secured
- [ ] CSRF protections implemented
- [ ] XSS protections implemented
- [ ] Proper session timeout implemented

## Error Handling
- [ ] No sensitive information in error messages
- [ ] Consistent error handling
- [ ] Failed security controls result in safe failures

## Dependency Security
- [ ] No known vulnerable dependencies
- [ ] Dependencies are up to date
- [ ] Minimal dependency usage

## Security Headers
- [ ] Appropriate security headers are set
- [ ] Content Security Policy implemented where appropriate