folder_name="$(basename $1)"
tar -cf - $1 | /homes/vpippi/gdrive/gdrive upload - "${folder_name}.tar.gz" -p "$2"
duration=$(( SECONDS - start ))
#echo $duration seconds