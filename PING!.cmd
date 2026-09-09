for /f "tokens=*" %i in ('gh pr list --repo LAF-US/IDAHO-VAULT --state open --json number --jq ".[].number"') do gh pr comment %i --repo LAF-US/IDAHO-VAULT --body "PING!"
