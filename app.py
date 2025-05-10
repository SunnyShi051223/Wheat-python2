import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

# --- 导入你的预测函数（下面我们稍后在 predict.py 中添加一个 predict_image 函数） ---
from predict import predict_image

# 配置
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 检查后缀
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 首页：上传表单
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 检查是否有文件
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # 保存到 uploads
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            # 调用预测
            pred_class, pred_probs = predict_image(save_path)
            # 渲染结果
            return render_template('index.html',
                                   filename=filename,
                                   pred_class=pred_class,
                                   pred_probs=pred_probs)
    return render_template('index.html')

# 让浏览器能访问上传的图片
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
