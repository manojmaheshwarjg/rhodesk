#!/bin/zsh
SP="$1"; LIST="$2"; DIR="$3"
mkdir -p "$SP/pages/$DIR"
while read -r u; do
  slug=$(echo "$u" | sed -e 's|https://www.rho.co||' -e 's|^/||' -e 's|/|__|g')
  [ -z "$slug" ] && slug="homepage"
  echo "$u|$SP/pages/$DIR/$slug.txt"
done < "$LIST" | tr '|' '\n' | xargs -n2 -P 8 python3 "$SP/fetch_page.py" > "$SP/fetchlog-$DIR.txt" 2>&1
echo "done $DIR: $(ls "$SP/pages/$DIR" | wc -l) files"
