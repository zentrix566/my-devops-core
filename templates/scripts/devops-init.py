import os
import shutil
import sys
import subprocess

# 强制 UTF-8 编码
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def run_command(cmd, msg):
    """辅助函数：执行命令并打印状态"""
    try:
        # shell=True 在 Windows 下兼容性更好
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ {msg}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ {msg} 失败 (请检查环境)")
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

    # 1. 原有文件同步逻辑
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
    print(f"✨ 文件同步完成！共处理 {success_count} 个文件。")

    # 2. 自动化进阶逻辑：Git 与 GitHub 交互
    print("\n--- 🌐 自动化交付扩展 ---")
    
    # 询问用户是否需要自动化 Git 操作
    choice = input("是否执行自动化 Git 初始化与配置推送? (y/n): ").strip().lower()
    
    if choice == 'y':
        # 2.1 Git 初始化
        if not os.path.exists(".git"):
            run_command("git init", "本地 Git 初始化")

        # 2.2 模拟注入 Secrets (通过 GitHub CLI)
        # 场景：自动为子项目配置 Docker 镜像仓库凭证
        print("🔐 正在检查 GitHub CLI 状态...")
        # 注意：这里假设你电脑已安装 gh 客户端并登录
        # 示例：设置子仓库的 DOCKER_USERNAME，此处仅为逻辑演示
        run_command(f"gh secret set DOCKER_USERNAME --body 'zentrix_admin'", "注入 GitHub Secrets")

        # 2.3 自动提交代码
        run_command("git add .", "暂存变更文件")
        run_command('git commit -m "chore: bootstrap devops environment by core-script"', "执行首次提交")

        print("\n🎉 [全链路就绪]")
        print("提示: 现在只需 git push，即可触发 GitHub Actions 流水线！")
    else:
        print("☕ 已跳过自动化 Git 操作。")

    print("=" * 40)

if __name__ == "__main__":
    init_project()