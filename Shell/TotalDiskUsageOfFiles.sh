
PATH="$DATA"
du -k $PATH/*.root | awk '{ total += $1 }; END { print total/(1024 * 1024)"GB" }'