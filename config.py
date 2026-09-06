"""Database/cloud credentials -- read from the environment, not hardcoded.

History note (intentional, for the Shaka test range): an earlier commit on
this branch hardcoded these same credentials directly in this file. They
were fake and never real, but were never rotated when this fix landed --
demonstrating exactly why a tree-only secret scan (trivy via --repo/--source)
gives a false sense of safety here, and why --trufflehog (full git-history
scan) exists.
"""

import os

AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
