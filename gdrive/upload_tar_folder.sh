!/bin/bash

# start=$SECONDS
folder_name="$(basename $2)"
tar -cf - $2 | $1 - "${folder_name}.tar.gz" -p "$3"
# duration=$(( SECONDS - start ))
#echo $duration seconds