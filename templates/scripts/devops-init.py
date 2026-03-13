import os
import shutil
import sys
import subprocess

# 强制 UTF-8 编码，解决 Windows 终端乱码
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def run_command(cmd, msg):
    """辅助函数：执行命令并静默处理"""
    try:
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ {msg}")
        return True
    except Exception:
        # 如果是 gh 命令失败，给一个友好的提示而不是直接报错
        if "gh " in cmd:
            print(f"💡 提示：{msg}跳过（需安装并登录 GitHub CLI）")
        else:
            print(f"❌ {msg} 失败")
        return False

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

    # --- 找回你的详细同步清单 ---
    success_count = 0
    for src_rel, dst_rel in files_to_sync:
        src = os.path.join(templates_path, src_rel)
        dst = os.path.join(target_path, dst_rel)
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(src, 'r', encoding='utf-8') as f:
                content = f.read()
            # 变量替换
            new_content = content.replace("{{APP_NAME}}", project_name)
            with open(dst, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ 已同步: {dst_rel}") # 恢复详细打印
            success_count += 1
        else:
            print(f"⚠️  跳过: 找不到 {src_rel}")

    print("-" * 40)
    print(f"✨ 文件处理完成！共同步 {success_count} 个文件。")

    # --- 自动化 Git/GitHub 扩展 ---
    print("\n--- 🌐 自动化交付扩展 ---")
    choice = input("是否执行自动化 Git 初始化与首次提交? (y/n): ").strip().lower()
    
    if choice == 'y':
        # 1. 初始化 Git
        if not os.path.exists(".git"):
            run_command("git init", "本地 Git 初始化")

        # 2. 尝试检查 GH CLI (可选功能)
        # 如果你没装 gh，这里会优雅地提示跳过
        # run_command("gh auth status", "检查 GitHub 登录状态")

        # 3. 自动提交
        run_command("git add .", "暂存变更文件 (git add)")
        run_command('git commit -m "chore: initial devops bootstrap"', "执行首次提交 (git commit)")

        print("\n🎉 [全链路就绪]")
        print(f"现在你可以运行: git push origin main")
    else:
        print("☕ 已跳过 Git 自动化操作。")

    print("=" * 40)

if __name__ == "__main__":
    init_project()