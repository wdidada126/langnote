#! /bin/bash
filename=boot
echo "$filename"
current_date=$(date +%m%d)
max_num=0
max_folder=""
folders=$(ls -d $filename$current_date*)
if [ -z "$folders" ]; then
    echo "文件夹为空"
else
    echo "$folders"
    sorted_folders=$(echo "$folders" | sort -r)
    echo "$sorted_folders"
    for folder in $sorted_folders; do
      num=$(echo "$folder" | cut -c 9-10)
      if [[ $num -gt $max_num ]]; then
        max_num=$num
        max_folder=$folder
      fi
    done
    ((max_num++))
    formatted_num=$(printf "%02d" $max_num)
    echo $formatted_num
fi
