# review_queue.md - Cola de Revisiones del Manager

> Entradas antiguas archivadas en .agent/collaboration/archive/review_queue_2026-06-11.md
> Solo se conservan las 10 revisiones mas recientes.

---

### MANAGER REVIEW - 2026-06-07 23:38:12
- **Plan ID:** WT-2026-237a
- **Decision:** TRANSPORT_FAILED
- **Source:** manager backend exec review

#### Summary
{"type":"error","timestamp":1780868292418,"sessionID":"ses_15bfa69aaffex6NBk5XgQdo17C","error":{"name":"APIError","data":{"message":"Your authentication token has been invalidated. Please try signing in again.","statusCode":401,"isRetryable":false,"responseHeaders":{"alt-svc":"h3=\":443\"; ma=86400","cf-cache-status":"DYNAMIC","cf-ray":"a082cc423c909bd2-MAD","connection":"keep-alive","content-length":"220","content-type":"text/plain","cross-origin-opener-policy":"same-origin-allow-popups","date":"Sun, 07 Jun 2026 21:37:24 GMT","nel":"{\"report_to\":\"cf-nel\",\"success_fraction\":0.01,\"max_age\":604800}","referrer-policy":"strict-origin-when-cross-origin","report-to":"{\"group\":\"cf-nel\",\"max_age\":604800,\"endpoints\":[{\"url\":\"https://a.nel.cloudflare.com/report/v4?s=JaEPD0R%2FNGQlsujs11OGcmjtYIw94TRT0NpUJBxbzyKBvShIWCQkVg92np2OpnjfCI3D0GFmGZxpahsrc7%2BTqydiFE99yFYU8D3ljhZ3R9SdjCUQRlt1UVCQhDjl\"}]}","server":"cloudflare","strict-transport-security":"max-age=31536000; includeSubDomains; preload","x-content-type-options":"nosniff","x-error-json":"ewogICJlcnJvciI6IHsKICAgICJtZXNzYWdlIjogIllvdXIgYXV0aGVudGljYXRpb24gdG9rZW4gaGFzIGJlZW4gaW52YWxpZGF0ZWQuIFBsZWFzZSB0cnkgc2lnbmluZyBpbiBhZ2Fpbi4iLAogICAgInR5cGUiOiAiaW52YWxpZF9yZXF1ZXN0X2Vycm9yIiwKICAgICJjb2RlIjogInRva2VuX2ludmFsaWRhdGVkIiwKICAgICJwYXJhbSI6IG51bGwKICB9LAogICJzdGF0dXMiOiA0MDEKfQ==","x-openai-authorization-error":"401","x-openai-ide-error-code":"token_invalidated","x-openai-internal-caller":"unknown_through_ide","x-openai-proxy-wasm":"v0.1","x-request-id":"4ce73cb2-568e-4cbb-b3a9-1cae3de5dac6","set-cookie":"__cf_bm=jcZNlCPs0UPnawEXItZuVdUdzD1PRbH75BaDabhaqms-1780868244.8398287-1.0.1.1-OGdP5mbau.G0zOklls34udug9DMn_4Uf8QBOoePlOdOmv4hvrUE8rnnVYuGOjQ8zczBn5ECmh35_kVFmQMYei9KqAMPyZKT7hP34rqJ_mQke252w_ukadsWGTaPobr2L; HttpOnly; SameSite=None; Secure; Path=/; Domain=chatgpt.com; Expires=Sun, 07 Jun 2026 22:07:24 GMT"},"responseBody":"{\n  \"error\": {\n    \"message\": \"Your authentication token has been invalidated. Please try signing in again.\",\n    \"type\": \"invalid_request_error\",\n    \"code\": \"token_invalidated\",\n    \"param\": null\n  },\n  \"status\": 401\n}","metadata":{"url":"https://api.openai.com/v1/responses"}}}}

---

### MANAGER REVIEW - 2026-06-08 16:44:09
- **Plan ID:** WT-2026-241a
- **Decision:** INSPECT
- **Source:** manager backend exec review

#### Summary

---

## SUMMARY
No se aprueba: el paquete muestra cambios fuera del whitelist y gates/evidencia incompletos.

---

## BLOCKERS
- `.agent/runtime/review_packets/WT-2026-241a_attempt-1.md:40-49` reporta cambios productivos en `.agent/agent_controller.py`, tests y docs, pero `work_plan.md` solo permite `scripts/launch_agent_terminals.ps1` -> limitar el ticket al archivo permitido o justificar/actualizar plan antes de implementar.
- `.agent/collaboration/execution_log.md:24-29` no registra `ruff check .` ni `python scripts/run_pytest_safe.py` como gates pasados -> ejecutar/registrar resultados o justificar formalmente según contrato.
- `scripts/launch_agent_terminals.ps1` diff líneas 638-640 llama `Stop-ProjectBuilderProcesses` de forma incondicional antes de `if ($LaunchBuilder)` -> debe ejecutarse solo cuando realmente se va a lanzar/relaunch/resume Builder para no cerrar Builders válidos en invocaciones sin Builder.

---

## SUGGESTIONS
- Añadir evidencia manual reproducible de la detección de procesos Builder por `project_root`.

DECISION: CHANGES

---

### MANAGER REVIEW - 2026-06-08 17:37:49
- **Plan ID:** WT-2026-242a
- **Decision:** INSPECT
- **Source:** manager backend exec review

#### Summary
Review complete. Found issues:
- Changed files exceed the whitelist: work_plan allows only `bus/review_bridge.py` and `tests/test_review_bridge.py`, but review packet shows additional productive motor changes in `.agent/agent_controller.py`, `scripts/launch_agent_terminals.ps1`, `tests/test_pre_handoff_multirepo.py`, `tests/unit/test_manager_approve.py`, and `docs/KNOWN_FAILURE_PATTERNS.md`.
- Quality gate evidence is missing from `execution_log.md`; it does not record exact pytest/ruff/validate commands, results, or numeric outcomes.
- Required governing tests for WT-2026-242a are not present in the review packet diff: executable off-PATH JSON attempt, unsupported-flag fallback, and textual APPROVE degradation after fallback.

DECISION: CHANGES

---

### MANAGER REVIEW - 2026-06-09 11:19:50
- **Plan ID:** WT-2026-244a
- **Decision:** INSPECT
- **Source:** manager backend exec review

#### Summary
Review complete. Found issues:
- Quality gate evidence is missing for WT-2026-244a: `execution_log.md` does not record the exact `validate --json` command, result, and numeric outcome/errors `{}`.
- Required Manager quality evidence for `ruff check .` and `python scripts/run_pytest_safe.py` is not present.
- Review packet reports changed files outside the allowed scope, including `.opencode/opencode.json` and motor tests, which violates `Files Likely Touched` / non-goals for this documentation-only ticket.

DECISION: CHANGES

---

### MANAGER REVIEW - 2026-06-09 18:14:02
- **Plan ID:** WT-2026-245a
- **Decision:** INSPECT
- **Source:** manager backend exec review

#### Summary
Review bridge blocked due to invalid ticket state.

---

### MANAGER REVIEW - 2026-06-10 11:54:24
- **Plan ID:** WT-2026-246a
- **Decision:** TRANSPORT_FAILED
- **Source:** manager backend exec review

#### Summary
{"type":"error","timestamp":1781085263865,"sessionID":"ses_14f0baf1dffekk9JF8D9czvSEY","error":{"name":"APIError","data":{"message":"Your authentication token has been invalidated. Please try signing in again.","statusCode":401,"isRetryable":false,"responseHeaders":{"alt-svc":"h3=\":443\"; ma=86400","cf-cache-status":"DYNAMIC","cf-ray":"a0977d5dd942780f-MAD","connection":"keep-alive","content-length":"220","content-type":"text/plain","cross-origin-opener-policy":"same-origin-allow-popups","date":"Wed, 10 Jun 2026 09:53:34 GMT","nel":"{\"report_to\":\"cf-nel\",\"success_fraction\":0.01,\"max_age\":604800}","referrer-policy":"strict-origin-when-cross-origin","report-to":"{\"group\":\"cf-nel\",\"max_age\":604800,\"endpoints\":[{\"url\":\"https://a.nel.cloudflare.com/report/v4?s=ueACWvRYP86wtce4aHZdzJWud6vBxG7SMu1Iir6fWmZAS9Mc2PWUqNUjA4Jp0GFlaPrBbV4nybMiEWA9Vl8y37wL6cJHoi1XOV6ML2iW%2FeWNk3sc%2BWYj1ZMz2oo0\"}]}","server":"cloudflare","strict-transport-security":"max-age=31536000; includeSubDomains; preload","x-content-type-options":"nosniff","x-openai-authorization-error":"identity_edge_internal_error","x-openai-ide-error-code":"token_invalidated","set-cookie":"__cf_bm=laaGP4Z6.WRlkwTcO.xVi7E033Dt0JwTvGoOhQbFqA4-1781085214.3964326-1.0.1.1-rL4htomhwGdYd1KHik2J6rJCxSjKnK665RjmRfebb3qhEVa_CDePHJoVq5dW.gqtmx._HtJyEbP_xZnOErCr9pea9THvJDU8LbukLi8b9BHrlMrd9yPyro5QNnWSdBIQ; HttpOnly; SameSite=None; Secure; Path=/; Domain=chatgpt.com; Expires=Wed, 10 Jun 2026 10:23:34 GMT"},"responseBody":"{\n  \"error\": {\n    \"message\": \"Your authentication token has been invalidated. Please try signing in again.\",\n    \"type\": \"invalid_request_error\",\n    \"code\": \"token_invalidated\",\n    \"param\": null\n  },\n  \"status\": 401\n}","metadata":{"url":"https://api.openai.com/v1/responses"}}}}

---

### MANAGER REVIEW - 2026-06-11 09:26:06
- **Plan ID:** WT-2026-249b
- **Decision:** INSPECT
- **Source:** manager backend exec review

#### Summary
Review complete. Found issues:
- Quality gate evidence is incomplete: execution_log shows only `pytest tests/test_agent_controller.py -k TestBuilderBriefExclusion -v`, not the full `tests/test_agent_controller.py -v` required by the work plan.
- Required gates from Manager contract are not evidenced: `ruff check .` and `python scripts/run_pytest_safe.py`.
- Review packet reports productive change in `.opencode/opencode.json`, outside Files Likely Touched and explicitly out of scope/non-goal for WT-2026-249b.

DECISION: CHANGES
