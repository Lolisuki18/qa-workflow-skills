# WCAG 2.2 AA quick checklist (manual and code checks)

Criterion numbers below are from WCAG 2.x. For wording, exceptions and the full list, read the official WCAG pages; do not quote criteria from memory when unsure.

| Area | Check | Criterion |
|---|---|---|
| Text alternatives | Informative images have alt text; decorative images have empty alt | 1.1.1 Non-text Content |
| Structure | Headings, lists, tables and landmarks use real elements; form fields have programmatic labels | 1.3.1 Info and Relationships |
| Contrast | Text contrast at least 4.5:1 (3:1 for large text); UI controls and focus indicators at least 3:1 | 1.4.3 Contrast (Minimum), 1.4.11 Non-text Contrast |
| Resize and reflow | Text zooms to 200% without loss; content reflows at 320 CSS px width without two-way scrolling | 1.4.4 Resize Text, 1.4.10 Reflow |
| Keyboard | Every function works with the keyboard alone | 2.1.1 Keyboard |
| No trap | Focus can always leave a component (dialogs, menus, widgets) | 2.1.2 No Keyboard Trap |
| Bypass | A skip link or landmarks let users jump past repeated blocks | 2.4.1 Bypass Blocks |
| Focus order | Tab order follows the visual and logical order | 2.4.3 Focus Order |
| Focus visible | The focused element is clearly visible | 2.4.7 Focus Visible |
| Target size | Pointer targets are at least 24 by 24 CSS px, or have enough spacing | 2.5.8 Target Size (Minimum) |
| Labels | Inputs have labels or instructions | 3.3.2 Labels or Instructions |
| Errors | Errors are identified in text and tied to the field | 3.3.1 Error Identification |
| Name, role, value | Custom controls expose name, role and state to assistive tech | 4.1.2 Name, Role, Value |
| Status messages | Success and error messages are announced without moving focus | 4.1.3 Status Messages |

## Keyboard walk-through (per flow)

1. Reload the page and press Tab from the top; note the first stops (skip link?).
2. Complete the flow without the mouse; every control reachable and operable (Enter, Space, arrows where expected).
3. Open and close dialogs and menus: focus moves in, is contained while open, returns to the trigger on close, Escape closes.
4. Submit a form with errors: focus or announcement leads to the first error.

## Screen-reader pass (only if one is available or the user ran it)

- Page title and headings give a usable outline; links and buttons make sense out of context.
- Inputs announce label, type, required state and errors.
- Dynamic updates (toasts, validation, loading) are announced.

## Automated tools

axe and Lighthouse find a subset of issues (commonly cited as well under half of all WCAG failures). A clean automated report never means the page is accessible. Record the tool, its version and the rule set used.

## Severity examples

- **Blocker:** checkout cannot be completed by keyboard; a modal traps focus.
- **Major:** form errors shown only in red with no text; unlabeled inputs.
- **Minor:** redundant alt text, heading levels skipped without confusing the outline.
