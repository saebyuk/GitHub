INSERT INTO pki_operation_history
(event_time, system_name, module_name, severity, error_code, message, operator_id, host_name, action_result)
VALUES
(NOW() - INTERVAL 1 DAY, 'PKI-Core', 'CRL-Validator', 'ERROR', 'PKI-CRL-001', 'CRL fetch timeout from internal CA endpoint', 'op001', 'pki-node-01', 'FAIL'),
(NOW() - INTERVAL 2 DAY, 'PKI-Core', 'OCSP-Validator', 'WARN', 'PKI-OCSP-004', 'OCSP responder latency exceeded threshold', 'op002', 'pki-node-02', 'RETRY'),
(NOW() - INTERVAL 3 DAY, 'PKI-Issue', 'Signer', 'ERROR', 'PKI-SIGN-008', 'Certificate chain validation failed for signing request', 'op003', 'pki-node-01', 'FAIL'),
(NOW() - INTERVAL 4 DAY, 'PKI-Auth', 'KeyStore', 'CRITICAL', 'PKI-KS-010', 'HSM key store access denied by policy', 'op004', 'pki-node-03', 'FAIL'),
(NOW() - INTERVAL 5 DAY, 'PKI-Issue', 'Cert-Renew', 'ERROR', 'PKI-CERT-015', 'Certificate expired before automated renewal', 'op001', 'pki-node-04', 'FAIL');
