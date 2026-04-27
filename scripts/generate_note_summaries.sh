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

month_tag_from_dir() {
  local year="$1"
  local month_dir="$2"
  local month_base
  month_base="$(basename "$month_dir")"
  if [[ "$month_base" =~ ^[0-9]{6}$ ]]; then
    printf '%s' "$month_base"
  elif [[ "$month_base" =~ ^[0-9]{1,2}$ ]]; then
    local month_num
    month_num=$((10#$month_base))
    printf '%s%02d' "$year" "$month_num"
  else
    printf '%s' "$month_base"
  fi
}

ensure_month_summary_file() {
  local year="$1"
  local month_dir="$2"
  local month_tag
  month_tag="$(month_tag_from_dir "$year" "$month_dir")"
  local existing
  existing="$(find "$month_dir" -maxdepth 1 -type f -name '*month*.md' | head -n 1 || true)"
  if [[ -n "$existing" ]]; then
    printf '%s' "$existing"
  else
    printf '%s/%s_month.md' "$month_dir" "$month_tag"
  fi
}

ensure_week_summary_files() {
  local year="$1"
  local month_dir="$2"
  local month_tag
  month_tag="$(month_tag_from_dir "$year" "$month_dir")"
  local any_file day_file day
  for week_no in 1 2 3 4 5; do
    any_file="$(find "$month_dir" -maxdepth 1 -type f \( -name "*week${week_no}.md" -o -name "*weekly_${week_no}.md" -o -name "*weekly${week_no}.md" -o -name "*_${week_no}_weekly.md" \) | head -n 1 || true)"
    if [[ -n "$any_file" ]]; then
      printf '%s\n' "$any_file"
      continue
    fi
    local start=$(( (week_no - 1) * 7 + 1 ))
    local end=$(( week_no * 7 ))
    [[ "$week_no" == "5" ]] && end=31
    day_file=""
    while IFS= read -r file; do
      day="$(basename "$file" .md)"
      day="${day:6:2}"
      day=$((10#$day))
      if (( day >= start && day <= end )); then
        day_file="$file"
        break
      fi
    done < <(month_days "$month_dir")
    if [[ -n "$day_file" ]]; then
      printf '%s/%s_week%s.md\n' "$month_dir" "$month_tag" "$week_no"
    fi
  done
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

find "$root" -maxdepth 1 -type d | sort | while IFS= read -r year_dir; do
  year="$(basename "$year_dir")"
  [[ "$year" =~ ^[0-9]{4}$ ]] || continue
  local_month_dirs=()
  while IFS= read -r line; do
    local_month_dirs+=("$line")
  done < <(find "$year_dir" -maxdepth 1 -mindepth 1 -type d | sort)

  for month_dir in "${local_month_dirs[@]}"; do
    while IFS= read -r week_file; do
      [[ -n "$week_file" ]] || continue
      generate_week "$week_file"
    done < <(ensure_week_summary_files "$year" "$month_dir")

    month_file="$(ensure_month_summary_file "$year" "$month_dir")"
    generate_month "$month_file"
  done

  generate_year "$year_dir"
done
