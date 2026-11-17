# Lab 5: Issues found in `ticket_booking_system.py`

Name: Ragul Rajkumar S | SRN: PES2UG24AM128 | Section: 5B

Before: Pylint 5.56/10, Flake8 7 warnings, Bandit 2 High + 1 Medium + 2 Low.
After: Pylint 10.00/10, Flake8 0 warnings, Bandit 0 issues.
Original reports are in `before/`, final reports are in the repo root.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| `eval()` on user-supplied promo text | Security (High, Bandit B307) | 42 | Any string passed as `promo_expr` runs as Python code, so a caller can run arbitrary commands or return a negative price. | Replaced with a numeric `discount_percent` that is validated to be 0-100. Price is computed with plain arithmetic. |
| `os.system("echo " + filename)` | Security (High, Bandit B605) | 58 | The filename is joined into a shell command, so a name like `x; rm -rf ~` is command injection. | Removed the shell call and used `print()`. Filename reduced with `os.path.basename`. |
| Hardcoded secret, printed to output | Security (High) | 70, 79 | `BOX_OFFICE_SECRET_PASS_2026` is in source control and also printed on screen. No tool flags the print, but the output looked wrong. | Key now comes from the `BOX_OFFICE_KEY` environment variable and is never printed. |
| MD5 for ticket hash | Security (High, Bandit B324) | 47 | MD5 is broken and collisions are easy to produce. | Switched to SHA-256. |
| `random` for booking PIN | Security (Low, Bandit B311) | 51 | `random` is predictable, so PINs can be guessed. | Used `secrets.randbelow`. |
| Mutable default argument `order_history=[]` | Bug (Pylint W0102) | 15 | The same list is shared by every call, so history leaks between calls. | Default is `None`; the list is only appended to when the caller passes one. |
| Bare `except: pass` in `cancel_seat` | Bug / Style (Flake8 E722, Bandit B110) | 24-27 | Hides every error, so cancelling an unknown seat silently does nothing and gives no feedback. | Removed try/except. The function checks the seat exists and returns True or False. |
| Function parameter shadows global `theater_seats` | Bug (Pylint W0621) | 61 | `get_theater_summary(theater_seats)` hides the module variable and is confusing. | Renamed the parameter to `seats` and used `sum()`. |
| Unused variables `booking_fee`, `base_price` | Style (Flake8 F841) | 31, 41 | Dead code. | Removed `booking_fee`; `base_price` is now used in the calculation. |
| Unused import `math` | Style (Flake8 F401) | 6 | Import never used. | Removed. |
| `== None` | Style (Flake8 E711) | 32 | Should compare with `is None`. | Replaced by `is not None` in a simplified one-line check. |
| `reserveSeat` camelCase name, no docstrings, file opened without `with`, no `__main__` guard, long line, no final newline | Style (Pylint C0103 / C0116 / R1732, Flake8 E501 / W292) | 15, 19, 55, 82 | Naming and structure do not follow PEP 8, and the file handle could leak on error. | Renamed to `reserve_seat`, added docstrings, used `with open(...)`, added `if __name__ == "__main__"`, wrapped lines. |
