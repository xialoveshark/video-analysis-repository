# video-analysis-repository
# Video Analysis System

## 项目简介
本项目是一个教育视频管理系统，旨在帮助教学秘书更高效地管理和分析教学视频。系统的核心功能包括视频上传、课程和教师信息管理、教学计划制定，以及视频内容的分析。项目基于前端后端分离架构，前端使用Vue.js，后端使用Flask框架，数据库采用MySQL进行存储。

## 项目背景
随着教育信息化和在线教育的快速发展，越来越多的高校开始采用教学视频作为重要的教学资源。然而，传统的视频分析方式主要依赖于人工方法，效率低下且难以保证准确性。本系统旨在通过视频转音频、音频转文本的方式，并结合大模型进行智能分析，提高教学视频管理和分析的效率。

## 核心功能
1. **视频上传**：用户可以通过系统上传教学视频，视频文件存储在服务器上，并记录视频的相关信息（如上传日期、课程名称、教师名称等）。
2. **课程和教师管理**：系统提供接口用于添加、修改和删除课程及教师信息，以便于视频的分类管理。
3. **教学计划管理**：用户可以通过上传CSV文件的方式批量导入教学计划，系统会自动解析CSV文件并将其导入数据库，同时用户也可以手动添加和修改教学计划。
4. **视频分析**：系统会对上传的视频文件转换为音频文件，音频文件转换为文本内容，并对文本内容进行智能分析，生成教学内容的参与度评分、互动性评分、正确性评分、深度和全面度评分、错误描述、修改建议等分析结果。

## 开发环境
- **操作系统**：Windows 11
- **开发工具**：PyCharm, VS Code
- **编程语言**：Python 3.12
- **数据库**：MySQL
- **运行环境**：本地服务器

## 项目地址
[https://github.com/xialoveshark/video-analysis-repository](https://github.com/xialoveshark/video-analysis-repository)

## 使用方法
1. 克隆仓库到本地：
   ```bash
   git clone https://github.com/xialoveshark/video-analysis-repository.git
   
2. 在backend目录中创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # 对于Windows系统，使用 `venv\Scripts\activate`

3. 安装后端依赖
pip install -r requirements.txt

4. 启动后端服务器
python app.py

5. 在frontend目录中安装前端依赖
npm install


6. 启动前端服务器
npm run serve

