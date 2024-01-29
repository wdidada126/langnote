#!/bin/bash  
set -e  
# 源文件夹路径  
src_dir="./"  
  
# 遍历源文件夹中的所有 .jar 文件  
for file in "$src_dir"/*.jar; do  
    # 获取文件的基本名称（不带路径）  
    # 文件路径
    file_path=$(basename "$file")  

	# 分割文件路径和文件名
	IFS='\' read -ra path_parts <<< "$file_path"
	filename="${path_parts[-1]}"

	# 构建目标路径
	target_path="."
	for ((i=0; i<${#path_parts[@]}-1; i++)); do
	  target_path+="/${path_parts[i]}"
	done

	# 创建目标文件夹
	mkdir -p "$target_path"

	# 复制文件
	cp "$file_path" "$target_path/$filename"
done
