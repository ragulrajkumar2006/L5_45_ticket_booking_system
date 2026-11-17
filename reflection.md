# Lab 5 Reflection

Name: Ragul Rajkumar S | SRN: PES2UG24AM128

(Written without the handout's exact question wording, so the answers are grouped by the usual four themes.)

**1. What kinds of problems did the tools catch, and which did they miss?**
Pylint caught style and design problems (naming, missing docstrings, the shadowed global, the mutable default argument). Flake8 caught formatting and dead code (unused import and variables, bare except, `== None`). Bandit caught the security problems (`eval`, the shell call, MD5, `random`). None of them flagged that the program prints a hardcoded secret, which I only noticed by reading the output. Tools find patterns, not intent.

**2. Which issues were most serious and why?**
`eval()` and `os.system` with user input, because either one lets an attacker run any command. Next were the hardcoded and printed secret, and weak hashing, which expose data. Style issues do not break anything but make the code harder to maintain.

**3. How did fixing one issue affect others?**
Removing `eval` changed the function's interface (a percentage instead of an expression), so `main` had to change. Removing the bare except forced me to decide what `cancel_seat` should return for an unknown seat. Renaming `reserveSeat` meant updating every call site.

**4. What would you do differently in a real project?**
Run the three tools in CI on every pull request so problems are caught early, keep secrets in environment variables or a secrets manager, and review tool output rather than only chasing the score. A 10/10 Pylint score does not prove the program is correct, so tests are still needed.
