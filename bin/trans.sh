#!/bin/bash

node_path="D:/GitHub Repository/note"
hexo_path="D:/GitHub Repository/tmp/blog"

function handle_file() {
  file_path="$1"
  file=$(basename "$file_path")
  if [[ "$file" =~ ^[a-z0-9_-]+.md$ ]]; then
    echo "handling $file"
    file_name=$(basename "$file" .md)
    hexo new "$file_name"
    path="$hexo_path/source/_posts/$file"
    cat "$file_path" >> "$path"
  fi
}

function get_files_or_dir() {
  file_list=$(ls "$1")

  for file in $file_list; do
    file_path="$1/$file"
    if test -f "$file_path"; then
      handle_file "$file_path"
    elif test -d "$file_path"; then
      get_files_or_dir "$file_path"
    fi
  done
}

get_files_or_dir "$node_path"
