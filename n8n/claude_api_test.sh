#!/usr/bin/env bash
# Smoke-test the Claude call outside n8n.  Usage: ANTHROPIC_API_KEY=sk-... ./claude_api_test.sh outputs/stats/Gita_2125422751.llm.txt
set -e
SYS=$(python3 - <<'PY'
import re,json;md=open('prompts/01_moment_miner_system_prompt.md').read();print(json.dumps(re.search(r'```text\n(.*?)\n```',md,re.S).group(1)))
PY
)
USR=$(python3 -c "import json,sys;print(json.dumps('<class_meta>{\"class_id\":\"test\",\"consent_on_file\":true}</class_meta>\n<transcript>\n'+open(sys.argv[1]).read()+'\n</transcript>'))" "$1")
curl -s https://api.anthropic.com/v1/messages -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2023-06-01" -H "content-type: application/json" \
 -d "{\"model\":\"claude-sonnet-5-5\",\"max_tokens\":4000,\"system\":$SYS,\"messages\":[{\"role\":\"user\",\"content\":$USR}]}"
