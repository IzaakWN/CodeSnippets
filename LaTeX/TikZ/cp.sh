mkdir -pv updated_20210808; cp -v `find . -type f -mtime -42 -print | grep -v .gz` updated_20210808/
rm -v updated_20210808/*gz; tar -cvzf updated_20210808.tar.gz updated_20210808; rm -rf updated_20210808
