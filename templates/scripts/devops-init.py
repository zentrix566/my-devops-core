import os
import shutil

def init_project(project_name):
    # 1. 自动获取当前脚本所在的绝对路径
    # script_dir 会指向 .../my-devops-core/templates/scripts/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. 定位到 templates 根目录 (scripts 的上一级)
    templates_path = os.path.dirname(script_dir)
    
    # 打印一下路径，方便你调试
    print(f"🔍 正在从模板目录读取: {templates_path}")

    # 3. 创建目标项目的目录结构
    os.makedirs("k8s-spec", exist_ok=True)
    os.makedirs(".github/workflows", exist_ok=True)

    # 4. 定义需要复制的文件列表
    files_to_copy = [
        ".dockerignore",
        "k8s-spec/deployment.yaml",
        "k8s-spec/service.yaml"
    ]

    for f_path in files_to_copy:
        src = os.path.join(templates_path, f_path)
        dst = os.path.join("./", f_path)
        
        if os.path.exists(src):
            # 如果是目录下的文件，确保目标子目录存在
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(src, dst)
            print(f"✅ 已同步: {f_path}")
        else:
            print(f"⚠️ 跳过: 找不到模板文件 {src}")

    # 5. 处理 GitHub Action 模板变量替换
    workflow_template = os.path.join(templates_path, "github-pipeline.yml")
    if os.path.exists(workflow_template):
        with open(workflow_template, "r", encoding="utf-8") as f:
            content = f.read()
            content = content.replace("{{APP_NAME}}", project_name)
        
        with open(".github/workflows/devops.yml", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 已生成 GitHub 流水线配置")

    print(f"\n🚀 项目 [{project_name}] 自动化接入完成！")

if __name__ == "__main__":
    # 获取当前运行脚本的文件夹名称作为项目名
    curr_dir_name = os.path.basename(os.getcwd())
    init_project(curr_dir_name)