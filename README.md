# Shaka Vulnerability Test Range

A small, deliberately vulnerable app kept around specifically to validate
[Shaka](https://github.com/KlausDREAD/shaka)'s scanners and for client demos.
**Every vulnerability here is intentional and every credential is fake.**
Do not deploy this publicly and do not reuse any value in it.

## What's planted, and what finds it

| Vulnerability | Where | Shaka flag |
|---|---|---|
| SQL injection (CWE-89), raw string interpolation | `app.py`, `/user?id=` | `--web` (nuclei), `--sqlmap` for confirmation + DBMS ID |
| Vulnerable dependencies (11 real CVEs across 3 packages) | `requirements.txt` | `--repo` / `--source` (trivy) |
| Hardcoded AWS + GitHub credentials | `config.py`, **only in git history** (removed from HEAD in the "rotate credentials" commit) | `--repo` / `--source` (trivy — finds nothing, correctly, since HEAD is clean) vs `--trufflehog` (finds them anyway, because history is where they still are) |

That last row is the point of this repo: it's a live, reproducible
demonstration of why `--trufflehog` exists. A tree-only secret scan (trivy)
gives a false sense of safety here — the credentials were "fixed" in the
sense that they're gone from the latest commit, but they were never rotated,
so anyone with clone access can still recover them from history.

## Using it

```bash
# Vulnerable deps + secret-history demo (no server needed)
shaka scan https://github.com/KlausDREAD/shaka-vuln-testbed \
  --no-recon --no-web --repo https://github.com/KlausDREAD/shaka-vuln-testbed --trufflehog

# SQL injection demo (needs the app actually running somewhere first --
# throwaway/local only, see the warning above)
pip install flask
python app.py &
shaka scan http://127.0.0.1:5000 --sqlmap --exploit
```
