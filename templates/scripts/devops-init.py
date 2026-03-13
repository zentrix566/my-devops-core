import os
import shutil
import sys

def init_project():
    # 1. 自动获取路径逻辑
    # 获取脚本自身绝对路径：E:\github\my-devops-core\templates\scripts\devops-init.py
    script_path = os.path.abspath(__file__)
    # 获取模板根目录：E:\github\my-devops-core\templates
    templates_path = os.path.dirname(os.path.dirname(script_path))
    
    # 2. 确定目标项目（当前运行脚本的目录）
    target_project_path = os.getcwd()
    project_name = os.path.basename(target_project_path)

    print(f"--- 🛠️  DevOps 自助化接入工具 ---")
    print(f"项目名称: {project_name}")
    print(f"模板来源: {templates_path}")
    print(f"目标路径: {target_project_path}\n")

    # 3. 定义需要同步的模板文件列表 (相对于 templates 目录)
    # 格式: (模板源文件路径, 目标文件路径)
    files_to_sync = [
        (".dockerignore", ".dockerignore"),
        ("k8s-spec/deployment.yaml", "k8s-spec/deployment.yaml"),
        ("k8s-spec/service.yaml", "k8s-spec/service.yaml"),
        ("github-pipeline.yml", ".github/workflows/devops.yml")
    ]

    # 4. 执行同步与变量渲染
    for src_rel, dst_rel in files_to_sync:
        src_path = os.path.join(templates_path, src_rel)
        dst_path = os.path.join(target_project_path, dst_rel)

        # 确保目标子目录存在
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)

        if os.path.exists(src_path):
            try:
                with open(src_path, 'r', encoding='utf-8') as f_src:
                    content = f_src.read()
                
                # 核心逻辑：渲染变量
                new_content = content.replace("{{APP_NAME}}", project_name)

                with open(dst_path, 'w', encoding='utf-8') as f_dst:
                    f_dst.write(new_content)
                
                print(f"✅ 已生成: {dst_rel}")
            except Exception as e:
                print(f"❌ 处理 {src_rel} 时出错: {e}")
        else:
            print(f"⚠️ 跳过: 模板中不存在 {src_rel}")

    # 5. 后续引导
    print(f"\n✨ 初始化完成！")
    print(f"👉 下一步操作：")
    print(f"   1. git add .")
    print(f"   2. git commit -m 'chore: bootstrap devops configs'")
    print(f"   3. git push origin main")
    print(f"\n🚀 随后前往 GitHub 仓库的 [Actions] 标签查看自动化流水线。")

if __name__ == "__main__":
    try:
        init_project()
    except KeyboardInterrupt:
        print("\n已取消操作")
        sys.exit(0)