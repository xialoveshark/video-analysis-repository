from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from apps import create_app
from apps.auth import Login, VideoDetail, VideoList, UploadVideo, AnalyzeVideo, UpdateVideo, AddCourse, \
    AddTeacher, AddCoursePlan, TeacherByName, CourseByName, CoursePlanList, TeacherList, CourseList, \
    VideoInformation, Register, DeleteTeacher, DeleteCourse, DeleteCoursePlan, DeleteVideo, UserLogs  # 更新导入路径

app = create_app()
api = Api(app)

# 注册API资源
api.add_resource(Login, '/api/login')
api.add_resource(VideoDetail, '/api/video/<int:video_id>')  # 视频详情API
api.add_resource(VideoList, '/api/videos')  # 视频列表API
api.add_resource(UploadVideo, '/api/video')  # 视频上传API
api.add_resource(AnalyzeVideo, '/api/analyze_video')
api.add_resource(UpdateVideo, '/api/video/<int:video_id>')
api.add_resource(AddCourse, '/api/course')
api.add_resource(AddTeacher, '/api/teacher')  # 确保路径与前端匹配
api.add_resource(AddCoursePlan, '/api/course_plan')
api.add_resource(TeacherByName, '/api/teacher_name/<string:teacher_name>')
api.add_resource(CourseByName, '/api/course_name/<string:course_name>')
api.add_resource(TeacherList, '/api/teachers')
api.add_resource(CourseList, '/api/courses')
api.add_resource(CoursePlanList, '/api/course_plans')
api.add_resource(VideoInformation, '/api/video_information')
api.add_resource(Register, '/api/register')
api.add_resource(DeleteTeacher, '/api/teacher/<int:teacher_id>')
api.add_resource(DeleteCourse, '/api/course/<int:course_id>')
api.add_resource(DeleteCoursePlan, '/api/course_plan/<int:course_id>/<int:teacher_id>/<int:week>')
api.add_resource(DeleteVideo, '/api/video/<int:video_id>')
api.add_resource(UserLogs, '/api/logs')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
