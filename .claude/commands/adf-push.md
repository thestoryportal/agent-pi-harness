---
description: Push ADF (agent-deployment-framework) main to origin from ArhuGula session.
allowed-tools: Bash
---

# Git Push — ADF

Check ADF branch and status:

```
git -C ~/Projects/agent-deployment-framework branch --show-current
git -C ~/Projects/agent-deployment-framework status
```

Confirm there are committed changes ahead of origin. Then output this command for the user to run:

```
! git -C ~/Projects/agent-deployment-framework push origin main
```

If the branch is not main, adjust accordingly and note it.
