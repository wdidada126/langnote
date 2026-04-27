#!/usr/bin/env bash
set -euo pipefail

root="${1:-.}"

trim() {
  local s="$1"
  s="${s#"${s%%[![:space:]]*}"}"
  s="${s%"${s##*[![:space:]]}"}"
  printf '%s' "$s"
}

extract_snippets() {
  local file="$1"
  awk '
    BEGIN { in_code = 0; count = 0 }
    /^```/ { in_code = !in_code; next }
    in_code { next }
    /^#/ { next }
    /^[[:space:]]*$/ { next }
    /^[[:space:]]*[-*][[:space:]]*\[[ xX]\]/ { next }
    /^[[:space:]]*```/ { next }
    {
      line = $0
      gsub(/\r/, "", line)
      sub(/^[[:space:]]*[-*][[:space:]]*/, "", line)
      sub(/^[[:space:]]*[0-9]+\.[[:space:]]*/, "", line)
      if (length(line) < 4) next
      if (line ~ /^https?:\/\//) next
      if (line ~ /^[[:space:]]*```/) next
      print line
      count++
      if (count >= 3) exit
    }
  ' "$file"
}

month_days() {
  local month_dir="$1"
  find "$month_dir" -maxdepth 1 -type f -name '*.md' \
    ! -name '*week*.md' ! -name '*weekly*.md' ! -name '*month*.md' ! -name '*year*.md' \
    | sort
}

existing_body() {
  local file="$1"
  if [[ -f "$file" ]]; then
    tail -n +2 "$file"
  fi
}

meaningful_count() {
  awk '
    /^## 原有内容$/ { next }
    /^## 整理补充$/ { next }
    NF { c++ }
    END { print c + 0 }
  '
}

generate_week() {
  local week_file="$1"
  local month_dir
  month_dir="$(dirname "$week_file")"
  local base
  base="$(basename "$week_file" .md)"
  local month_tag="${base:0:6}"
  local week_no
  week_no="$(printf '%s' "$base" | sed -E 's/.*[^0-9]([1-5])$/\1/')"
  [[ "$week_no" =~ ^[1-5]$ ]] || return 0

  local start=$(( (week_no - 1) * 7 + 1 ))
  local end=$(( week_no * 7 ))
  if [[ "$week_no" == "5" ]]; then
    end=31
  fi

  local day_files=()
  while IFS= read -r line; do
    day_files+=("$line")
  done < <(month_days "$month_dir" | awk -v s="$start" -v e="$end" '
    {
      file = $0
      gsub(/.*\//, "", file)
      day = substr(file, 7, 2) + 0
      if (day >= s && day <= e) print $0
    }
  ')

  local tmp
  tmp="$(mktemp)"
  local original_body
  original_body="$(existing_body "$week_file")"
  {
    printf '# %s\n\n' "$base"
    if [[ "$(printf '%s\n' "$original_body" | meaningful_count)" -gt 0 ]]; then
      printf '## 原有内容\n\n'
      printf '%s\n' "$original_body"
      printf '\n## 整理补充\n\n'
    fi
    printf '## 时间范围\n\n'
    printf -- '- %s 月第 %s 周\n\n' "$month_tag" "$week_no"
    printf '## 本周记录\n\n'
    if ((${#day_files[@]} == 0)); then
      printf -- '- 本周暂无可汇总的日记内容。\n'
    else
      local file date snippets line
      for file in "${day_files[@]}"; do
        date="$(basename "$file" .md)"
        local snippets=()
        while IFS= read -r line; do
          snippets+=("$line")
        done < <(extract_snippets "$file")
        if ((${#snippets[@]} == 0)); then
          printf -- '- %s：补充了当日日志，暂未提炼出明确主题。\n' "$date"
        else
          printf -- '- %s：' "$date"
          local first=1
          for line in "${snippets[@]}"; do
            line="$(trim "$line")"
            [[ -n "$line" ]] || continue
            if (( first )); then
              printf '%s' "$line"
              first=0
            else
              printf '；%s' "$line"
            fi
          done
          printf '\n'
        fi
      done
    fi
  } > "$tmp"
  mv "$tmp" "$week_file"
}

generate_month() {
  local month_file="$1"
  local month_dir
  month_dir="$(dirname "$month_file")"
  local base
  base="$(basename "$month_file" .md)"

  local week_files=()
  while IFS= read -r line; do
    week_files+=("$line")
  done < <(find "$month_dir" -maxdepth 1 -type f \( -name "${base:0:6}_week*.md" -o -name "${base:0:6}_weekly*.md" -o -name "${base:0:6}_*weekly*.md" \) | sort)
  local day_files=()
  while IFS= read -r line; do
    day_files+=("$line")
  done < <(month_days "$month_dir")

  local tmp
  tmp="$(mktemp)"
  local original_body
  original_body="$(existing_body "$month_file")"
  {
    printf '# %s\n\n' "$base"
    if [[ "$(printf '%s\n' "$original_body" | meaningful_count)" -gt 0 ]]; then
      printf '## 原有内容\n\n'
      printf '%s\n' "$original_body"
      printf '\n## 整理补充\n\n'
    fi
    printf '## 本月概览\n\n'
    printf -- '- 本月共整理 %s 篇日记。\n' "${#day_files[@]}"
    printf -- '- 已结合周报回填当月重点主题，便于后续继续补充。\n\n'
    printf '## 周度脉络\n\n'
    if ((${#week_files[@]} == 0)); then
      printf -- '- 本月暂无周报文件。\n'
    else
      local wf first_line second_line
      for wf in "${week_files[@]}"; do
        first_line="$(awk 'NF && $0 !~ /^#/ { print; exit }' "$wf")"
        second_line="$(awk 'seen && NF { print; exit } /^## 本周记录$/ { seen=1 }' "$wf")"
        printf -- '- %s：' "$(basename "$wf" .md)"
        if [[ -n "$(trim "${second_line:-}")" ]]; then
          printf '%s\n' "$(trim "$second_line")"
        elif [[ -n "$(trim "${first_line:-}")" ]]; then
          printf '%s\n' "$(trim "$first_line")"
        else
          printf '已建立周总结。\n'
        fi
      done
    fi
    printf '\n## 本月高频主题\n\n'
    if ((${#day_files[@]} == 0)); then
      printf -- '- 本月暂无日记内容。\n'
    else
      local sample_count=0 file line
      for file in "${day_files[@]}"; do
        while IFS= read -r line; do
          line="$(trim "$line")"
          [[ -n "$line" ]] || continue
          printf -- '- %s\n' "$line"
          sample_count=$((sample_count + 1))
          [[ "$sample_count" -ge 12 ]] && break 2
        done < <(extract_snippets "$file")
      done
    fi
  } > "$tmp"
  mv "$tmp" "$month_file"
}

generate_year() {
  local year_dir="$1"
  local year
  year="$(basename "$year_dir")"
  local year_file="$year_dir/${year}_year.md"

  local month_files=()
  while IFS= read -r line; do
    month_files+=("$line")
  done < <(find "$year_dir" -maxdepth 2 -type f -name "${year}[0-1][0-9]_month.md" | sort)
  local tmp
  tmp="$(mktemp)"
  local original_body
  original_body="$(existing_body "$year_file")"
  {
    printf '# %s_year\n\n' "$year"
    if [[ "$(printf '%s\n' "$original_body" | meaningful_count)" -gt 0 ]]; then
      printf '## 原有内容\n\n'
      printf '%s\n' "$original_body"
      printf '\n## 整理补充\n\n'
    fi
    printf '## 年度概览\n\n'
    printf -- '- 本年已整理 %s 个月度总结。\n' "${#month_files[@]}"
    printf -- '- 内容主要来自对应月份的日记与周报回填结果。\n\n'
    printf '## 月度摘要\n\n'
    if ((${#month_files[@]} == 0)); then
      printf -- '- 本年暂无月度总结文件。\n'
    else
      local mf line
      for mf in "${month_files[@]}"; do
        line="$(awk 'NF && $0 !~ /^#/ && $0 !~ /^##/ { print; exit }' "$mf")"
        printf -- '- %s：%s\n' "$(basename "$mf" .md)" "${line:-已完成月度整理。}"
      done
    fi
  } > "$tmp"
  mv "$tmp" "$year_file"
}

for year in 2024 2025 2026; do
  year_dir="$root/$year"
  [[ -d "$year_dir" ]] || continue
  while IFS= read -r week_file; do
    generate_week "$week_file"
  done < <(find "$year_dir" -type f \( -name '*week*.md' -o -name '*weekly*.md' \) | sort)

  while IFS= read -r month_file; do
    generate_month "$month_file"
  done < <(find "$year_dir" -type f -name '*month*.md' | sort)

  generate_year "$year_dir"
done
