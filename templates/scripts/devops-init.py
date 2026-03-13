import os
import shutil
import sys

# 强制 UTF-8 编码
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def init_project():
    script_path = os.path.abspath(__file__)
    templates_path = os.path.normpath(os.path.join(os.path.dirname(script_path), ".."))
    target_path = os.getcwd()
    project_name = os.path.basename(target_path)

    print("=" * 40)
    print(f"🚀 DevOps 脚手架启动")
    print(f"📍 脚本位置: {script_path}")
    print(f"📂 模板目录: {templates_path}")
    print(f"🎯 目标项目: {target_path}")
    print("=" * 40)

    files_to_sync = [
        (".dockerignore", ".dockerignore"),
        ("k8s-spec/deployment.yaml", "k8s-spec/deployment.yaml"),
        ("k8s-spec/service.yaml", "k8s-spec/service.yaml"),
        ("github-pipeline.yml", ".github/workflows/devops.yml")
    ]

    success_count = 0
    for src_rel, dst_rel in files_to_sync:
        src = os.path.join(templates_path, src_rel)
        dst = os.path.join(target_path, dst_rel)
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(src, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = content.replace("{{APP_NAME}}", project_name)
            with open(dst, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ 已同步: {dst_rel}")
            success_count += 1
        else:
            print(f"⚠️  跳过: 找不到 {src_rel}")

    print("=" * 40)
    print(f"✨ 任务完成！同步了 {success_count} 个文件。")


if __name__ == "__main__":
    init_project()