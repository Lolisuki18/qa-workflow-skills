# Exploratory Charters & Manual Run Scripts

For `Manual` cases and deliberate "break the app" sessions. Everything below is a **suggestion** — choose by the actual feature, do not apply mechanically. Record a result only when the user (or you, if you truly could run it) actually observed it.

## 1. Quick Manual Run Script

Group cases by module/flow to reduce context switching. Template:

```markdown
### Group: <Module / flow> — setup: <accounts, data, URL: [Needs input if unknown]>

| # | TC ID | Steps | Data | Expected result | Result (Pass/Fail/Blocked) | Notes/Evidence |
|---|---|---|---|---|---|---|
| 1 | TC-LOGIN-001 | 1. Open /login 2. Enter ... 3. Click Login | ... | ... | ☐ | |
```

Rules: order cases so data-creating cases run before data-using ones, but still write pre-conditions so each case can run on its own; P0 first; leave the result cell blank for the user.

## 2. Session-Based Exploratory Charter

One charter (30–60 minutes):

```markdown
**Charter:** Explore <area> using <approach/data> to discover <type of risk>
**Duration:** 45 min | **Role used:** <role> | **Environment:** [Needs input]
**Record:** bugs found · questions · new test ideas · areas not reached
```

Illustrative charters:
- Explore the signup form with boundary data and special characters to find validation/storage errors.
- Explore the payment flow with repeated actions and interruptions to find duplicate orders/state mismatch.
- Explore the admin screens with a low-privilege account to find permission holes.

End of session: summarize bugs (→ `qa-defect-writer`), open unknowns (→ ask), remaining risk areas.

## 3. "Break the app" catalogue

### Repeated actions & timing
- **Double-click / rapid clicks** on submit, pay, create → duplicate records/double charge? Is the button disabled while processing?
- Submit the form from **two tabs** at once; open the same record in two tabs, then edit/delete.
- Press Enter repeatedly in an input.

### Navigation
- **Back / Forward** after submit, mid multi-step flow, after logout (can a private page be viewed from cache?).
- **Reload (F5)** mid-flow: is typed data lost? Does resubmission create duplicates?
- Close the tab/browser mid-way and reopen; open a deep link while logged out; edit IDs in the URL.

### Network & server
- **Lose network** mid-submit (turn off Wi-Fi or DevTools offline): which message, is data lost, is retry safe?
- **Slow network** (throttling "Slow 3G"): spinner, timeout, users clicking again.
- Server error responses (500/timeout) → is the message friendly without exposing sensitive technical detail?

### Session & permissions
- Session expires while filling a long form; login on two devices; log out in another tab then act in this one.
- Open a higher role's URL/function directly with a low-privilege account; change another user's resource ID.

### File upload/download
- **Heavy** file over the limit, exactly at the limit; **0-byte** file; **wrong format** (rename `.exe` to `.jpg`); very long/accented/special/duplicate file names; multiple files; cancel mid-upload; lose network during upload.

### Input data
- Empty, whitespace only, very long; `' " < > & % \`; accented text, emoji, RTL characters; pasted text with newlines; negative/0/huge/decimal numbers; Feb 29, time zones, past/future dates.
- Script/HTML/SQL-like strings to check that **the project's own** system escapes properly. Never try them against systems you are not authorized to test.

### UI & environment
- Shrink the window/phone screen, 200% zoom, rotate the screen; other browsers; cookies/JavaScript off if supported; dark mode; keyboard (Tab/Enter/Esc) and basic screen reader.

### Existing data
- Duplicates (already-registered email); deleted record whose link remains; empty/very long lists; deleting something still referenced.

## 4. Recording anomalies

1. Stop at the moment it happens; note the exact steps that led to it.
2. Capture a screenshot/log/Network tab (HAR) if possible; note the time.
3. Try to reproduce ≥ 2 times; record the ratio (e.g. "2/3 times") — never say "always" before trying.
4. Record the **real** environment in use (do not remember → ask/write `[Needs input]`).
5. Hand over to `qa-defect-writer`.

## 5. Prompt to the user after manual runs

> Have you finished the "<Module>" group? For each TC tell me: Pass / Fail / Blocked, and for Fail the symptom + screenshot/log if available. Cases not yet run stay `Not Run`.
