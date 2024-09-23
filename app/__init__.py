from flask import Flask, render_template, send_from_directory
import os

from app.extensions import check_ip_whitelist, db, login_manager
from blueprints import blueprints


def create_app():
    app = Flask(__name__)

    match os.getenv('FLASK_ENV').lower:
        case 'development':
            app.config.from_object('config.DevelopmentConfig')
        case 'testing':
            app.config.from_object('config.TestingConfig')
        case 'production':
            app.config.from_object('config.ProductionConfig')
        case _:
            # Placeholder for error
            app.config.from_object('config.DevelopmentConfig')

    # Initialize extensions
    check_ip_whitelist(app.config.GEOIP_DB, app.config.ALLOWED_COUNTRIES)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'welcome'

    # Register the blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    # Basic routes


    @app.route("/welcome")
    def welcome():
        return render_template('welcome.html', title='Welcome')



    @app.route("/")
    def home():
        return render_template('home.html')


    # Other routes
    @app.route("/images")
    def images():
        image_dir = os.path.join("static", "labs", "lr6", "PhotoOut")
        valid_extensions = {'.png', '.jpg', '.jpeg', '.gif'}
        images = [image for image in os.listdir(image_dir)
                  if os.path.splitext(image)[1].lower() in valid_extensions]
        images = [os.path.join("labs", "lr6", "PhotoOut", image).replace("\\", "/") for image in images]
        return render_template('images.html', images=images)

    @app.route("/videos")
    def videos():
        video_dir = os.path.join("static", "labs", "lr7", "VideoOut")
        valid_extensions = {'.avi', '.mpeg', '.mp4'}
        videos = [video for video in os.listdir(video_dir)
                  if os.path.splitext(video)[1].lower() in valid_extensions]
        videos = os.listdir(video_dir)
        videos = [os.path.join("labs", "lr7", "VideoOut", video).replace("\\", "/") for video in videos]
        return render_template('videos.html', videos=videos)

    def rename_lab(lab_name):
        match = re.match(r'lr(\d+)([a-z]*)', lab_name)
        if match:
            lab_number = match.group(1)
            suffix = match.group(2)
            if suffix:
                return f"Лабораторная работа №{lab_number.upper()}{suffix}"
            else:
                return f"Лабораторная работа №{lab_number}"
        else:
            return lab_name

    LABS_DIR = os.path.join(app.static_folder, 'labs')

    @app.route("/works")
    def works():
        labs = []
        for lab_name in os.listdir(LABS_DIR):
            lab_path = os.path.join(LABS_DIR, lab_name)
            if os.path.isdir(lab_path):
                lab_files = {'pdf': None, 'scripts': []}
                for file_name in os.listdir(lab_path):
                    file_path = os.path.join(lab_path, file_name)
                    if file_name.endswith('.pdf'):
                        lab_files['pdf'] = file_name
                    elif file_name.endswith('.bat') or file_name.endswith('.sh'):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as file:
                                script_content = file.read()
                            lab_files['scripts'].append({'name': file_name, 'content': script_content})
                        except UnicodeDecodeError:
                            with open(file_path, 'r', encoding='latin-1') as file:
                                script_content = file.read()
                            lab_files['scripts'].append({'name': file_name, 'content': script_content})
                labs.append({'name': lab_name, 'files': lab_files, 'heading': rename_lab(lab_name)})
        return render_template('labs.html', labs=labs)

    @app.route('/labs/<lab_name>/<file_name>')
    def download_file(lab_name, file_name):
        return send_from_directory(os.path.join(LABS_DIR, lab_name), file_name)

    @app.route("/diagram")
    def diagram():
        return render_template("diagram.html")

    @app.route('/review')
    def review():
        return render_template("review.html")

    return app
