# multi-catch

```shell
try {
			// 保存文件
			file.transferTo(dest);
			// 保存成功
			mv.addObject("success", true);
			mv.addObject("msg", "上传文件成功");
		} catch (IllegalStateException | IOException e) {
			// 保存失败
			mv.addObject("success", false);
			mv.addObject("msg", "上传文件失败");
			e.printStackTrace();
		}
    
    
Error:(44, 48) java: -source 1.5 中不支持 multi-catch 语句
  (请使用 -source 7 或更高版本以启用 multi-catch 语句)
```
