# Non-functional catalog

Pick only what the feature needs. Thresholds below are prompts for a conversation, not defaults to apply silently.

## 1. Performance (NF-PERF)

| Scenario | Metric | Notes |
|---|---|---|
| Page or API under normal load | p50 / p95 response time | Threshold from SLA; ask if missing |
| Peak load | Error rate, throughput at N concurrent users | Ramp up gradually |
| Stress | Point where errors start; recovery after load stops | Test environment only |
| Soak | Memory and latency drift over time | Long run; schedule with the user |
| Large data | Behaviour with many rows, big uploads | Use realistic volumes |
| Front end | Load time, largest content paint, bundle size | Lighthouse or the browser performance panel |

## 2. Security basics (NF-SEC)

Black-box checks a QA can run safely on a test environment. For code-level review use `security-reviewer`.

- Authentication: lockout or throttling after repeated failures, session expiry, logout invalidates the session.
- Authorization: user A cannot reach user B's data or admin pages by changing ids or URLs.
- Input handling: special characters, scripts and SQL-like text are stored or shown as plain data, not executed.
- Transport and headers: HTTPS only, cookies `HttpOnly` / `Secure`, security headers present.
- Error pages do not reveal stack traces or internal paths.
- Passive scan (for example OWASP ZAP baseline) on the test URL, with findings triaged by hand.

## 3. Accessibility (NF-A11Y)

- Target level: ask (commonly WCAG 2.1 or 2.2 level AA).
- Keyboard only: every action reachable, visible focus, no keyboard trap, logical tab order.
- Screen reader: labels on inputs and buttons, headings structure, alt text, error messages announced.
- Colour contrast and zoom to 200% without loss of content.
- Automated scan (axe, Lighthouse) catches only part of the issues: say so, and add manual checks for key flows.

## 4. Compatibility (NF-COMP)

- Browser and version matrix from the requirements or analytics, not from guesses.
- Mobile and desktop viewports; orientation changes; touch vs mouse.
- Operating system and device specifics when the product is a mobile or desktop app.
- Locale, time zone and date/number formats.

## 5. Usability and localization (NF-USA)

- Task completion for the top 3 user tasks, with a count of steps and clear error recovery.
- Labels and messages consistent with the glossary; no truncated text in other languages or long strings.
- Right-to-left or non-Latin scripts where supported.

## 6. CLI and local tools (NF-PERF / NF-SEC)

- Performance with growing data: run time and memory at 10x and 100x the normal row count; report the curve, not one number.
- Data safety: write interrupted midway (kill the process), corrupt or truncated input file, empty file, wrong encoding, read-only folder.
- Concurrency: two runs on the same data file at once; is data lost or corrupted?
- Report-only measurements without an approved threshold get status `Informational`.

## Case row example

```text
| NF-PERF-01 | Performance | GET /products with 50 concurrent users for 5 min | p95 < [Needs input: SLA] ms, errors < 1% | k6 | staging-test | P1 | R12 |
```
