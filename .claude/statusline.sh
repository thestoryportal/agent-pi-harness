#!/usr/bin/env bash
# ArhuGula status line — extends user's base statusline with harness info

CYAN='\033[38;5;81m'
PURPLE='\033[38;5;141m'
YELLOW='\033[38;5;221m'
GREEN='\033[38;5;114m'
DIMWHITE='\033[2;37m'
BLUE='\033[38;5;111m'
RED='\033[38;5;203m'
RESET='\033[0m'
BOLD='\033[1m'

input=$(cat)

cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // ""')
model=$(echo "$input" | jq -r '.model.display_name // ""')
used_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
session_name=$(echo "$input" | jq -r '.session_name // empty')
vim_mode=$(echo "$input" | jq -r '.vim.mode // empty')

home="$HOME"
short_cwd="${cwd/#$home/\~}"

seg_count=$(echo "$short_cwd" | tr -cd '/' | wc -c | tr -d ' ')
if [ "$seg_count" -gt 4 ]; then
  short_cwd="…/$(echo "$short_cwd" | rev | cut -d'/' -f1-4 | rev)"
fi

branch=""
git_status_str=""
if git -C "$cwd" rev-parse --git-dir > /dev/null 2>&1; then
  branch=$(git -C "$cwd" -c gc.auto=0 symbolic-ref --short HEAD 2>/dev/null \
           || git -C "$cwd" -c gc.auto=0 rev-parse --short HEAD 2>/dev/null)

  porcelain=$(git -C "$cwd" -c gc.auto=0 status --porcelain 2>/dev/null)
  modified=$(echo "$porcelain" | grep -c '^.M' 2>/dev/null || echo 0)
  staged=$(echo "$porcelain"   | grep -c '^[MADRCU]' 2>/dev/null || echo 0)
  untracked=$(echo "$porcelain"| grep -c '^??' 2>/dev/null || echo 0)
  deleted=$(echo "$porcelain"  | grep -c '^.D' 2>/dev/null || echo 0)

  [ "$modified"  -gt 0 ] && git_status_str="${git_status_str}!${modified}"
  [ "$staged"    -gt 0 ] && git_status_str="${git_status_str}+${staged}"
  [ "$untracked" -gt 0 ] && git_status_str="${git_status_str}?${untracked}"
  [ "$deleted"   -gt 0 ] && git_status_str="${git_status_str}✘${deleted}"

  upstream=$(git -C "$cwd" -c gc.auto=0 rev-parse --abbrev-ref '@{upstream}' 2>/dev/null)
  if [ -n "$upstream" ]; then
    ahead=$(git -C "$cwd" -c gc.auto=0 rev-list --count "@{upstream}..HEAD" 2>/dev/null || echo 0)
    behind=$(git -C "$cwd" -c gc.auto=0 rev-list --count "HEAD..@{upstream}" 2>/dev/null || echo 0)
    [ "$ahead"  -gt 0 ] && git_status_str="${git_status_str}⇡${ahead}"
    [ "$behind" -gt 0 ] && git_status_str="${git_status_str}⇣${behind}"
  fi
fi

line=""

# ArhuGula harness badge
line="${line}$(printf "${BOLD}${RED}⚙ ArhuGula${RESET}")"
line="${line}$(printf "${DIMWHITE} hooks:13 fail-open${RESET}")"
line="${line} $(printf "${DIMWHITE}│${RESET}") "

# Original status line items
line="${line}$(printf "${BOLD}${CYAN}%s${RESET}" "$short_cwd")"

if [ -n "$branch" ]; then
  line="${line} $(printf "${BOLD}${PURPLE} %s${RESET}" "$branch")"
fi

if [ -n "$git_status_str" ]; then
  line="${line} $(printf "${BOLD}${YELLOW}%s${RESET}" "$git_status_str")"
fi

if [ -n "$model" ]; then
  line="${line} $(printf "${GREEN}[%s]${RESET}" "$model")"
fi

if [ -n "$used_pct" ]; then
  used_int=$(printf '%.0f' "$used_pct")
  line="${line} $(printf "${BOLD}${YELLOW}ctx:%s%%${RESET}" "$used_int")"
fi

if [ -n "$session_name" ]; then
  line="${line} $(printf "${BLUE}\"%s\"${RESET}" "$session_name")"
fi

if [ -n "$vim_mode" ]; then
  line="${line} $(printf "${BOLD}${YELLOW}[%s]${RESET}" "$vim_mode")"
fi

line="${line} $(printf "${DIMWHITE}%s${RESET}" "$(date +%H:%M)")"

printf "%b\n" "$line"
