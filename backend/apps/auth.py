import string
import random
import requests
import werkzeug
from flask import jsonify, send_file, session, request
from flask_restful import Resource, reqparse
from sparkai.core.messages import ChatMessage
from werkzeug.utils import secure_filename
from exts import db
from apps.models import Account, Video, CoursePlan, Course, Teacher, TC, UD, UserActionLog
import bcrypt
import os
import json
import time
from moviepy.editor import VideoFileClip
from datetime import datetime
from .utils.AuthV4Util import addAuthParams
import re
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from captcha.image import ImageCaptcha

SLICE_SIZE = 10485760

APP_KEY = '67d6fe5ed8e82ce2'
APP_SECRET = 'TwHszYHsm6Yxdcp0YKQYhDGsZONKoxOm'

SPARKAI_URL = "wss://spark-api.xf-yun.com/v3.5/chat"
SPARKAI_APP_ID = "22c862db"
SPARKAI_API_SECRET = "ZDZlMTliOWU4NWViODUwMjMyMDA4Njhk"
SPARKAI_API_KEY = "e2df7a01bbf1fe203de100c0d0dbb8a7"
SPARKAI_DOMAIN = "generalv3.5"

# 确保创建tmp目录
os.makedirs(os.path.join(os.path.dirname(__file__), 'tmp'), exist_ok=True)

task0 = """
你将收到一段语音转文字记录，请你完成以下任务，并以结构化数据的形式返回结果：
1. 找出所有的错字和别字，重复的句子或字词，和其他文本记录的错误。
2. 修改这些错字和别字，删去重复的句子或字词和其他文本记录的错误。在此之外，不要做其他修改。
3. 返回包含原始文本、修改后文本和错误列表的结构化数据，格式如下：
```json
{
  "原始文本": "<original_text>",
  "修改后文本": "<corrected_text>",
  "错误列表": [
    {
      "位置": "<error_position>",
      "错误类型": "<error_type>",
      "原始内容": "<original_content>",
      "修改内容": "<corrected_content>"
    }
  ]
}
```
"""


task1 = """
你将收到两段文本：第一段是课程记录文本，其中记录了课上师生所有对话的文字记录；
第二段是关于课程教学目标和涵盖知识点的描述。
请你完成以下任务，并以干净的JSON格式返回结果：
一、评分：请根据以下四个方面对课程进行评分，每个方面的评分范围是1到5的整数，1代表非常差，5代表非常好。
```json
{
  "讲解清晰度": <score>,
  "互动性": <score>,
  "参与度": <score>,
  "准确度": <score>,
  "深度和全面度": <score>
}
```
二、错误说明：指出课程记录文本中出现的错误，忽略包括错字、重复句子等可能是录入错误的部分，并解释这些错误是什么。如果没有识别到错误，请返回“无”。
```json
{
  "错误": [
    {
      "位置": "<error_position>",
      "描述": <error_description>
    }
  ]
}
```
三、改正错误后记录文本：基于你识别出的错误，请提供一个改正错误后的课程记录文本。
```json
{
  "改正后的文本": "<corrected_text>"
}
```
四、总体评价：对这次课程进行总体评价，包括优点、缺点和改进建议。
```json
{
  "总体评价": "<overall_evaluation>"
}
```
"""


class Login(Resource):
    def options(self):
        return '', 204  # OPTIONS 请求的处理

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='Username cannot be blank')
        parser.add_argument('password', required=True, help='Password cannot be blank')
        data = parser.parse_args()

        username = data['username']
        password = data['password']

        account = Account.query.filter_by(username=username).first()
        if account and bcrypt.checkpw(password.encode('utf-8'), account.password_hash.encode('utf-8')):
            log = UserActionLog(
                user_id=account.account_id,
                action_type="login",
                description=f"用户 {username} 登录成功"
            )
            db.session.add(log)
            db.session.commit()
            session['user_id'] = account.account_id
            session.modified = True  # 确保会话修改被保存
            print(f"Set session user_id: {account.account_id}")
            return {"message": "登录成功", "account_id": account.account_id}, 200
        else:
            log = UserActionLog(
                user_id=None,  # 如果需要记录尝试登录的用户，可以在数据库设计中允许 user_id 为 null
                action_type="login_fail",
                description=f"用户 {username} 登录失败"
            )
            db.session.add(log)
            db.session.commit()
            return {"message": "用户名或密码错误"}, 401



class VideoDetail(Resource):
    def get(self, video_id):
        video = Video.query.get(video_id)
        if video:
            return {
                "video_id": video.video_id,
                "title": video.title,
                "upload_account": video.upload_account,
                "upload_date": video.upload_date.isoformat(),
                "course_id": video.course_id,
                "teacher_id": video.teacher_id,
                "week": video.week,
                "video_path": video.video_path,
                "clarity_rating": video.clarity_rating,
                "interactivity_rating": video.interactivity_rating,
                "engagement_rating": video.engagement_rating,
                "correctness_rating": video.correctness_rating,
                "content_depth_rating": video.content_depth_rating,
                "error_description": video.error_description,
                "correction": video.correction,
                "comments": video.comments
            }, 200
        else:
            return {"message": "视频未找到"}, 404


class VideoList(Resource):
    def get(self):
        videos = Video.query.all()
        return [{
            "video_id": video.video_id,
            "title": video.title,
            "video_path": video.video_path
        } for video in videos], 200


class UploadVideo(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, help='Title cannot be blank')
        parser.add_argument('upload_account', required=True, help='Upload account cannot be blank')
        parser.add_argument('upload_date', required=True, help='Upload date cannot be blank')
        parser.add_argument('course_id', required=True, help='Course ID cannot be blank')
        parser.add_argument('teacher_id', required=True, help='Teacher ID cannot be blank')
        parser.add_argument('week', required=True, help='Week cannot be blank')
        parser.add_argument('error_description', required=True, help='Error description cannot be blank')
        parser.add_argument('video_path', required=True, help='Video path cannot be blank') # 使用路径字段
        data = parser.parse_args()

        # 打印收到的数据以调试
        print("Received data:", data)

        # Convert upload_date string to datetime object
        upload_date = datetime.strptime(data['upload_date'], '%Y-%m-%d')

        new_video = Video(
            title=data['title'],
            video_path=data['video_path'], # 使用传递过来的路径
            upload_account=data['upload_account'],
            upload_date=upload_date,
            course_id=data['course_id'],
            teacher_id=data['teacher_id'],
            week=data['week'],
            error_description=data['error_description']
        )

        db.session.add(new_video)
        db.session.commit()

        return {"message": "视频上传成功"}, 201


class UpdateVideo(Resource):
    def put(self, video_id):
        video = Video.query.get(video_id)
        if not video:
            return {"message": "视频未找到"}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('clarity_rating', type=int, required=False)
        parser.add_argument('interactivity_rating', type=int, required=False)
        parser.add_argument('engagement_rating', type=int, required=False)
        parser.add_argument('correctness_rating', type=int, required=False)
        parser.add_argument('content_depth_rating', type=int, required=False)
        parser.add_argument('error_description', type=str, required=False)
        parser.add_argument('correction', type=str, required=False)
        parser.add_argument('comments', type=str, required=False)
        data = parser.parse_args()

        if data['clarity_rating'] is not None:
            video.clarity_rating = data['clarity_rating']
        if data['interactivity_rating'] is not None:
            video.interactivity_rating = data['interactivity_rating']
        if data['engagement_rating'] is not None:
            video.engagement_rating = data['engagement_rating']
        if data['correctness_rating'] is not None:
            video.correctness_rating = data['correctness_rating']
        if data['content_depth_rating'] is not None:
            video.content_depth_rating = data['content_depth_rating']
        if data['error_description'] is not None:
            video.error_description = data['error_description']
        if data['correction'] is not None:
            video.correction = data['correction']
        if data['comments'] is not None:
            video.comments = data['comments']

        db.session.commit()
        return {"message": "视频信息更新成功"}, 200


class AnalyzeVideo(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('video_id', required=True, help='Video ID cannot be blank')
        data = parser.parse_args()

        video = Video.query.get(data['video_id'])
        if not video:
            return {"message": "视频未找到"}, 404

        # 确保视频路径是绝对路径
        base_path = 'D:\\videosystem\\my-project\\public'
        video_path = os.path.join(base_path, video.video_path.strip("\\/"))
        des_path = os.path.join(os.path.dirname(__file__), 'tmp', f'{video.video_id}.txt')

        course_plan = CoursePlan.query.filter_by(course_id=video.course_id, teacher_id=video.teacher_id,
                                                 week=video.week).first()
        if not course_plan:
            return {"message": "课程计划未找到"}, 404

        goal = course_plan.goal

        try:
            analysis_result = video2text(video_path, des_path, goal)
            video.clarity_rating = analysis_result["评分"]["讲解清晰度"]
            video.interactivity_rating = analysis_result["评分"]["互动性"]
            video.engagement_rating = analysis_result["评分"]["参与度"]
            video.correctness_rating = analysis_result["评分"]["准确度"]
            video.content_depth_rating = analysis_result["评分"]["深度和全面度"]
            video.error_description = json.dumps(analysis_result["错误"], ensure_ascii=False)
            video.correction = analysis_result["改正后的文本"]
            video.comments = analysis_result["总体评价"]

            db.session.commit()
            return analysis_result, 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"message": str(e)}, 500


def video2audio(video_path, audio_path, start_time=0, end_time=None):
    # 确保目标目录存在
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)

    video = VideoFileClip(video_path)
    my_audio_clip = video.audio
    audio_subclip = my_audio_clip.subclip(start_time, end_time)
    audio_subclip.write_audiofile(audio_path)
    return audio_path


def video2text(video_path, des_path, goal):
    # 使用一个临时目录来存储音频文件
    audio_path = os.path.join(os.path.dirname(__file__), 'tmp', 'tmp.wav')
    video2audio(video_path, audio_path)
    print("成功转音频")

    j = createRequest(audio_path)
    print("成功转写")
    text = process_json_data(j)
    # print(text)  # temporary
    # print(len(text))  # temporary
    res = process_text_with_goal(text, goal)
    return res


def createRequest(PATH):
    file_len = os.path.getsize(PATH)
    slice_num = int(file_len / SLICE_SIZE) + (0 if (file_len % SLICE_SIZE == 0) else 1)
    prepare_result = prepareHelper(PATH, file_len, slice_num)
    print('prepase_result:' + prepare_result)
    prepare_result_json = json.loads(prepare_result)
    if prepare_result_json["errorCode"] != "0":
        exit(0)
    taskId = prepare_result_json["result"]

    file = open(PATH, 'rb')
    try:
        sliceId = 1
        while True:
            content = file.read(SLICE_SIZE)
            if not content or len(content) == 0:
                break
            files = {'file': content}
            upload_result = uploadHelper(taskId, sliceId, files)
            print('upload_result:' + upload_result + '  sliceId:' + str(sliceId))
            upload_result_json = json.loads(upload_result)
            if upload_result_json["errorCode"] != "0":
                exit(0)
            sliceId += 1
    finally:
        file.close()

    merge_result = mergeHelper(taskId)
    print('merge_result:' + merge_result)
    merge_result_json = json.loads(merge_result)
    if merge_result_json["errorCode"] != "0":
        exit(0)

    while True:
        print('sleep a while')
        time.sleep(20)
        get_process_result = getProcessHelper(taskId)
        print('get_process_result:' + get_process_result)
        get_process_result_json = json.loads(get_process_result)
        if get_process_result_json["errorCode"] == "0":
            result = get_process_result_json["result"]
            item = result[0]
            if item["status"] == "9":
                print('任务处理成功')
                break
        else:
            print('任务处理失败')
            exit(0)

    get_result_result, s = getResultHelper(taskId)
    return get_result_result.json()


def prepareHelper(PATH, file_len, slice_num):
    lang_type = 'zh-CHS'
    name = os.path.basename(PATH)
    format = os.path.splitext(PATH)[-1][1:]
    type = '1'
    hotword = ""

    data = {'name': name, 'format': format, 'langType': lang_type, 'sliceNum': str(slice_num),
            'fileSize': str(file_len), 'type': type, 'needSpeakerId': 1, 'hotWords': hotword}
    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/api/audio/prepare', header, data, 'post')
    return str(res.content, 'utf-8')


def uploadHelper(taskId, sliceId, file):
    type = '1'
    data = {'q': taskId, 'sliceId': sliceId, 'type': type, 'file': file}
    addAuthParams(APP_KEY, APP_SECRET, data)
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = requests.post('https://openapi.youdao.com/api/audio/upload', data, files=file)
    return str(res.content, 'utf-8')


def mergeHelper(taskId):
    data = {'q': taskId}
    addAuthParams(APP_KEY, APP_SECRET, data)
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/api/audio/merge', header, data, 'post')
    return str(res.content, 'utf-8')


def getProcessHelper(taskId):
    data = {'q': taskId}
    addAuthParams(APP_KEY, APP_SECRET, data)
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/api/audio/get_progress', header, data, 'post')
    return str(res.content, 'utf-8')


def getResultHelper(taskId):
    data = {'q': taskId}
    addAuthParams(APP_KEY, APP_SECRET, data)
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/api/audio/get_result', header, data, 'post')
    return res, str(res.content, 'utf-8')


def process_json_data(json_data):
    l = json_data['result']
    ans = []
    las = ''
    sen = ''

    for i in l:
        p = i['speaker']
        w = i['sentence']
        if p == las:
            sen += w
        else:
            if las:
                ans.append([las, sen])
            sen = w
            las = p

    ans.append([las, sen])

    res = ""
    for speaker, sen in ans:
        res += f"{speaker}: {sen}\n"

    return res


def process_text_with_goal(text, goal):
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
        request_timeout=100  # 设置请求超时时间为60秒
    )

    def process_chunk(chunk):
        messages = [
            ChatMessage(role="system", content=task0),
            ChatMessage(role="user", content=chunk),
        ]
        handler = ChunkPrintHandler()
        response = spark.generate([messages], callbacks=[handler])
        generated_text = response.generations[0][0].text

        pattern = r'```json\n({.*?})\n```'
        matches = re.findall(pattern, generated_text, re.DOTALL)

        if matches:
            try:
                json_object = json.loads(matches[0])
                new_text = json_object['修改后文本']
            except json.JSONDecodeError as e:
                new_text = chunk
        else:
            new_text = chunk
        return new_text

    # 分割文本
    chunks = [text[i:i + 1000] for i in range(0, len(text), 1000)]
    corrected_chunks = [process_chunk(chunk) for chunk in chunks]
    corrected_text = ' '.join(corrected_chunks)

    content = f"记录文本：{corrected_text}\n{goal}"
    messages1 = [
        ChatMessage(role="system", content=task1),
        ChatMessage(role="user", content=content),
    ]

    handler = ChunkPrintHandler()
    response = spark.generate([messages1], callbacks=[handler])
    generated_text = response.generations[0][0].text

    json_objects = []
    pattern = r'```json\n({.*?})\n```'
    matches = re.findall(pattern, generated_text, re.DOTALL)
    for match in matches:
        try:
            json_objects.append(json.loads(match))
        except json.JSONDecodeError as e:
            pass

    if len(json_objects) != 4:
        return {"error": "Expected 4 JSON objects but got a different number."}

    result = {
        "评分": json_objects[0],
        "错误": json_objects[1]['错误'],
        "改正后的文本": json_objects[2]['改正后的文本'],
        "总体评价": json_objects[3]['总体评价']
    }
    return result


def doCall(url, header, params, method):
    if method == 'get':
        return requests.get(url, params=params, headers=header)
    elif method == 'post':
        return requests.post(url, data=params, headers=header)


class AddCourse(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('course_name', required=True, help='Course name cannot be blank')
        parser.add_argument('course_description', required=True, help='Description cannot be blank')
        parser.add_argument('duration', required=True, type=int, help='Duration cannot be blank')
        parser.add_argument('university', required=True, help='University cannot be blank')
        parser.add_argument('department', required=True, help='Department cannot be blank')
        parser.add_argument('video_num', required=True, type=int, help='Video number cannot be blank')
        parser.add_argument('avg_clarity_rating', type=float, required=False)
        parser.add_argument('avg_interactivity_rating', type=float, required=False)
        parser.add_argument('avg_engagement_rating', type=float, required=False)
        parser.add_argument('avg_correctness_rating', type=float, required=False)
        parser.add_argument('avg_content_depth_rating', type=float, required=False)
        data = parser.parse_args()

        new_course = Course(
            course_name=data['course_name'],
            course_description=data['course_description'],
            duration=data['duration'],
            university=data['university'],
            department=data['department'],
            video_num=data['video_num'],
            avg_clarity_rating=data.get('avg_clarity_rating'),
            avg_interactivity_rating=data.get('avg_interactivity_rating'),
            avg_engagement_rating=data.get('avg_engagement_rating'),
            avg_correctness_rating=data.get('avg_correctness_rating'),
            avg_content_depth_rating=data.get('avg_content_depth_rating')
        )

        db.session.add(new_course)
        db.session.commit()

        # 记录日志
        user_id = session.get('user_id')
        if user_id:
            log = UserActionLog(
                user_id=user_id,
                action_type='AddCourse',
                description=f'User {user_id} added course {new_course.course_name}'
            )
            db.session.add(log)
            db.session.commit()

        return {"message": "课程添加成功"}, 201


class AddTeacher(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('teacher_name', required=True, help='Teacher name cannot be blank')
        parser.add_argument('department', required=True, help='Department cannot be blank')
        parser.add_argument('university', required=True, help='University cannot be blank')
        parser.add_argument('video_num', type=int, required=True, help='Video number cannot be blank')
        parser.add_argument('avg_clarity_rating', type=float, required=True, help='Average clarity rating cannot be blank')
        parser.add_argument('avg_interactivity_rating', required=True, help='Average interactivity rating cannot be blank')
        parser.add_argument('avg_engagement_rating', required=True, help='Average engagement rating cannot be blank')
        parser.add_argument('avg_correctness_rating', required=True, help='Average correctness rating cannot be blank')
        parser.add_argument('avg_content_depth_rating', required=True, help='Average content depth rating cannot be blank')
        data = parser.parse_args()

        new_teacher = Teacher(
            teacher_name=data['teacher_name'],
            department=data['department'],
            university=data['university'],
            video_num=data['video_num'],
            avg_clarity_rating=data['avg_clarity_rating'],
            avg_interactivity_rating=data['avg_interactivity_rating'],
            avg_engagement_rating=data['avg_engagement_rating'],
            avg_correctness_rating=data['avg_correctness_rating'],
            avg_content_depth_rating=data['avg_content_depth_rating']
        )

        db.session.add(new_teacher)
        db.session.commit()

        # 记录日志
        user_id = session.get('user_id')
        if user_id:
            log = UserActionLog(
                user_id=user_id,
                action_type='AddTeacher',
                description=f'User {user_id} added teacher {new_teacher.teacher_name}'
            )
            db.session.add(log)
            db.session.commit()
        else:
            print("user_id is null in session")

        return {"message": "教师添加成功"}, 201


class AddCoursePlan(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('course_id', type=int, required=True, help='Course ID cannot be blank')
        parser.add_argument('teacher_id', type=int, required=True, help='Teacher ID cannot be blank')
        parser.add_argument('week', type=int, required=True, help='Week cannot be blank')
        parser.add_argument('goal', required=True, help='Goal cannot be blank')
        parser.add_argument('key_point', required=True, help='Key point cannot be blank')
        data = parser.parse_args()

        # 检查 tc 表中是否存在对应的 course_id 和 teacher_id 组合
        tc_record = TC.query.filter_by(course_id=data['course_id'], teacher_id=data['teacher_id']).first()
        if not tc_record:
            # 如果不存在，创建一个新的组合并提交
            new_tc_record = TC(course_id=data['course_id'], teacher_id=data['teacher_id'])
            db.session.add(new_tc_record)
            db.session.commit()  # 提交事务，确保新的组合被添加到 tc 表中

        new_course_plan = CoursePlan(
            course_id=data['course_id'],
            teacher_id=data['teacher_id'],
            week=data['week'],
            goal=data['goal'],
            key_point=data['key_point']
        )

        db.session.add(new_course_plan)
        db.session.commit()

        return {"message": "教学计划添加成功"}, 201


class TeacherByName(Resource):
    def get(self, teacher_name):
        teacher = Teacher.query.filter_by(teacher_name=teacher_name).first()
        if teacher:
            return {"teacher_id": teacher.teacher_id}, 200
        else:
            return {"message": "教师未找到"}, 404


class CourseByName(Resource):
    def get(self, course_name):
        course = Course.query.filter_by(course_name=course_name).first()
        if course:
            return {"course_id": course.course_id}, 200
        else:
            return {"message": "课程未找到"}, 404


class TeacherList(Resource):
    def get(self):
        teachers = Teacher.query.all()
        return [{'teacher_id': t.teacher_id, 'teacher_name': t.teacher_name, 'department': t.department, 'university': t.university, 'video_num': t.video_num} for t in teachers]


class CourseList(Resource):
    def get(self):
        courses = Course.query.all()
        return [{'course_id': c.course_id, 'course_name': c.course_name, 'course_description': c.course_description, 'duration': c.duration, 'university': c.university, 'department': c.department, 'video_num': c.video_num} for c in courses]


class CoursePlanList(Resource):
    def get(self):
        course_plans = db.session.query(CoursePlan, Teacher.teacher_name, Course.course_name).join(Teacher, CoursePlan.teacher_id == Teacher.teacher_id).join(Course, CoursePlan.course_id == Course.course_id).all()
        return [{'course_id': cp.CoursePlan.course_id, 'course_name': cp.course_name, 'teacher_id': cp.CoursePlan.teacher_id, 'teacher_name': cp.teacher_name, 'week': cp.CoursePlan.week, 'goal': cp.CoursePlan.goal, 'key_point': cp.CoursePlan.key_point} for cp in course_plans]


class VideoInformation(Resource):
    def get(self):
        videos = Video.query.all()
        return [{'video_id': v.video_id, 'title': v.title, 'upload_account': v.upload_account, 'upload_date': v.upload_date.isoformat(), 'course_id': v.course_id, 'teacher_id': v.teacher_id, 'week': v.week, 'video_path': v.video_path, 'clarity_rating': v.clarity_rating, 'interactivity_rating': v.interactivity_rating, 'engagement_rating': v.engagement_rating, 'correctness_rating': v.correctness_rating, 'content_depth_rating': v.content_depth_rating, 'error_description': v.error_description, 'correction': v.correction, 'comments': v.comments} for v in videos]


class Register(Resource):
    def options(self):
        return '', 204  # OPTIONS 请求的处理

    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        university = data.get('university')
        department = data.get('department')

        if Account.query.filter_by(username=username).first():
            return {"message": "用户名已存在"}, 400

        # 检查并添加新的 university 和 department 组合
        ud_record = UD.query.filter_by(university=university, department=department).first()
        if not ud_record:
            new_ud = UD(university=university, department=department)
            db.session.add(new_ud)
            db.session.commit()

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        new_account = Account(
            username=username,
            password_hash=password_hash,
            created_date=datetime.utcnow(),
            university=university,
            department=department
        )
        db.session.add(new_account)
        db.session.commit()

        return {"message": "注册成功"}, 201


class DeleteTeacher(Resource):
    def delete(self, teacher_id):
        cascade = request.args.get('cascade', 'false').lower() == 'true'
        teacher = Teacher.query.get(teacher_id)
        if teacher:
            if cascade:
                # 级联删除相关联的数据
                db.session.query(CoursePlan).filter_by(teacher_id=teacher_id).delete()
                db.session.query(Video).filter_by(teacher_id=teacher_id).delete()
            else:
                # 检查是否有相关联的数据
                if db.session.query(CoursePlan).filter_by(teacher_id=teacher_id).count() > 0 or \
                   db.session.query(Video).filter_by(teacher_id=teacher_id).count() > 0:
                    return {"message": "该教师有相关联的数据，不能删除"}, 400

            db.session.delete(teacher)
            db.session.commit()
            return {"message": "教师删除成功"}, 200
        return {"message": "教师未找到"}, 404


class DeleteCourse(Resource):
    def delete(self, course_id):
        cascade = request.args.get('cascade', 'false').lower() == 'true'
        course = Course.query.get(course_id)
        if course:
            if cascade:
                # 级联删除相关联的数据
                db.session.query(CoursePlan).filter_by(course_id=course_id).delete()
                db.session.query(Video).filter_by(course_id=course_id).delete()
            else:
                # 检查是否有相关联的数据
                if db.session.query(CoursePlan).filter_by(course_id=course_id).count() > 0 or \
                   db.session.query(Video).filter_by(course_id=course_id).count() > 0:
                    return {"message": "该课程有相关联的数据，不能删除"}, 400

            db.session.delete(course)
            db.session.commit()
            return {"message": "课程删除成功"}, 200
        return {"message": "课程未找到"}, 404


class DeleteCoursePlan(Resource):
    def delete(self, course_id, teacher_id, week):
        cascade = request.args.get('cascade', 'false').lower() == 'true'
        course_plan = CoursePlan.query.filter_by(course_id=course_id, teacher_id=teacher_id, week=week).first()
        if course_plan:
            if cascade:
                # 级联删除相关联的数据
                db.session.query(Video).filter_by(course_id=course_id, teacher_id=teacher_id, week=week).delete()
            else:
                # 检查是否有相关联的数据
                if db.session.query(Video).filter_by(course_id=course_id, teacher_id=teacher_id, week=week).count() > 0:
                    return {"message": "该教学计划有相关联的视频数据，不能删除"}, 400

            db.session.delete(course_plan)
            db.session.commit()
            return {"message": "教学计划删除成功"}, 200
        return {"message": "教学计划未找到"}, 404


class DeleteVideo(Resource):
    def delete(self, video_id):
        video = Video.query.get(video_id)
        if video:
            db.session.delete(video)
            db.session.commit()
            return {"message": "视频删除成功"}, 200
        return {"message": "视频未找到"}, 404


class UserLogs(Resource):
    def get(self):
        user_id = request.args.get('user_id')
        if not user_id:
            return {"message": "user_id is required"}, 400

        logs = UserActionLog.query.filter_by(user_id=user_id).all()
        return [{
            "id": log.id,
            "timestamp": log.timestamp.isoformat(),
            "action_type": log.action_type,
            "description": log.description
        } for log in logs], 200

# class Captcha(Resource):
#     def get(self):
#         image = ImageCaptcha()
#         captcha_text = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
#         session['captcha'] = captcha_text
#         data = image.generate(captcha_text)
#         return send_file(data, mimetype='image/png')
