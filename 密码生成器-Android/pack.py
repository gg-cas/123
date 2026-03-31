"""将 Android 项目打包为 ZIP"""
import os, zipfile

project_dir = r"C:\Users\lenovo\WorkBuddy\20260330173521\password-android"
out_zip = r"C:\Users\lenovo\Desktop\密码生成器-Android项目.zip"

skip_dirs = {'.gradle', 'build', '__pycache__', '.idea'}
skip_exts = {'.pyc'}

count = 0
with zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for root, dirs, files in os.walk(project_dir):
        # 过滤目录
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            if any(f.endswith(e) for e in skip_exts):
                continue
            fp = os.path.join(root, f)
            arc = os.path.join("密码生成器-Android", os.path.relpath(fp, project_dir))
            zf.write(fp, arc)
            count += 1

size_mb = os.path.getsize(out_zip) / 1024 / 1024
print(f"打包完成: {out_zip}")
print(f"文件数: {count}, 大小: {size_mb:.2f} MB")
