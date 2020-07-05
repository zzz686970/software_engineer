find /path/to/files -type f -name '*.jpg' -mtime +30 -exec rm {} \;
find /path/to/files -type f -name '*.jpg' -mtime +30 -exec mv {} /path/to/archive \;