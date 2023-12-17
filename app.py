from flask import Flask,request,jsonify,send_file
from flask_restful import Resource,Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from models import User,Role,Song,Album,db,Playlist,UserRating
from flask_security import SQLAlchemyUserDatastore,Security,roles_required,auth_token_required
import bcrypt
import csv
from flask_cors import CORS
import os
import base64
from io import BytesIO
import datetime
from datetime import datetime
from werkzeug.utils import cached_property
from werkzeug.utils import secure_filename
from celery_worker import make_celery
import smtplib
import crontab
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from jinja2 import Template
from weasyprint import HTML
import uuid
from email import encoders
from celery.result import AsyncResult
import matplotlib.pyplot as plt
from flask_caching import Cache


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music_streaming_database.sqlite3'
app.config['SECRET_KEY'] = 'onepieceisreal'
app.config['SECURITY_PASSWORD_SALT'] = 'onepieceisreal'
app.config['SQLALCHEMY_TRACK_MODIFICATONS'] = False
app.config['WTF_CSRF_ENABLED']=False
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER']='Authentication-Token'
app.config['SECURITY_TOKEN_AUTHENTICATION_KEY'] = 'token'
# app.config['CELERY_BROKER_URL']='redis://localhost:6379/0'
# app.config['CELERY_RESULT_BACKEND']='redis://localhost:6379/0'
# app.config['CACHE_TYPE']='RedisCache'
# app.config['CACHE_REDIS_HOST']='localhost'
# app.config['CACHE_REDIS_PORT']='6379'
# SMTP_SERVER_HOST='localhost'
# SMTP_SERVER_PORT='1025'
# SENDER_ADDRESS='griss.harris@gmail.com'
# SENDER_PASSWORD=''
db.init_app(app)
api = Api(app) 
cache=Cache(app)
CORS(app, origins='http://localhost:8080',supports_credentials=True)
user_datastore=SQLAlchemyUserDatastore(db,User,Role)
app.security = Security(app, user_datastore)
# celery = make_celery(app)

class UserLoginAPI(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        print(username)
        password = data.get('password')
        user = user_datastore.find_user(username=username)
        print(user.username)
        if user:
            if not user.is_admin:
                user.last_login = datetime.now()
                db.session.commit()
                hashed_password = user.password.encode('utf-8')
                is_password_valid = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
                if is_password_valid:
                    token = user.get_auth_token()  
                    return jsonify({"message": "User Successfully Logged In", "id": user.id, "token": token})
                else:
                    return jsonify("Invalid password")
        else:
            return jsonify("NOT USER!!!!!")  

class CreatorLoginAPI(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        print(username)
        password = data.get('password')
        user = user_datastore.find_user(username=username)
        print(user.username)
        if user:
            user.last_login = datetime.now()
            db.session.commit()
            hashed_password = user.password.encode('utf-8')
            is_password_valid = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
            if is_password_valid:
                token = user.get_auth_token()  
                return jsonify({"message": "Creator Successfully Logged In", "id": user.id, "token": token})
            else:
                return jsonify("Invalid password")
        else:
            return jsonify("NOT USER!!!!!") 

class AdminLoginAPI(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        print(username)
        password = data.get('password')
        user = user_datastore.find_user(username=username)
        print(user.username)
        if user:
            if user.is_admin:
                user.last_login = datetime.now()
                db.session.commit()
                print(user)
                hashed_password = user.password.encode('utf-8')
                is_password_valid = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
                if is_password_valid:
                    token = user.get_auth_token()  
                    print(token)
                    return jsonify({"message": "Admin Successfully Logged In", "id": user.id, "token": token})
                else:
                    return jsonify("Invalid password")
        else:
            return jsonify("NOT USER!!!!!")        

class UserAPI(Resource):
    @roles_required('user')
    @auth_token_required
    @cache.cached(timeout=50)
    def get(self, id=None):
        user = user_datastore.find_user(id=id)
        print(user.roles)
        if user:
            user_json = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
            return jsonify(user_json)
        else:
            return jsonify(message="User not found"), 404  
    def post(self):
        data=request.get_json()
        username=data.get('username')
        password=data.get('password')
        email=data.get('email')
        report=data.get('reportType')
        user_role = user_datastore.find_or_create_role(name='user',description='user has access')
        user=user_datastore.create_user(
        username=username,
        password= bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        email=email,
        active=True,
        report=report,
        roles=[user_role],
        is_admin=False
        )
        db.session.commit()
        return jsonify("User Successfully Registered")

class CreatorAPI(Resource):
    @roles_required('creator')
    @auth_token_required
    @cache.cached(timeout=50)
    def get(self, id=None):
        user = user_datastore.find_user(id=id)
        print(user.roles)
        if user:
            user_json = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
            return jsonify(user_json)
        else:
            return jsonify(message="Creator not found"), 404  
    def post(self):
        data=request.get_json()
        username=data.get('username')
        password=data.get('password')
        email=data.get('email')
        user = user_datastore.find_user(username=username)
        print(user.roles)
        if not user:
            creator_role = user_datastore.find_or_create_role(name='creator',description='creator has access')
            user=user_datastore.create_user(
            username=username,
            password= bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            email=email,
            active=True,
            roles=[creator_role],
            is_admin=False)
        else:
            user_role = user_datastore.find_or_create_role(name='user',description='user has access')
            creator_role = user_datastore.find_or_create_role(name='creator',description='creator has access')
            user.roles=[user_role,creator_role]
            # if user_role not in user.roles:
            #     user.roles.append(user_role)
            #     return jsonify("Creator Role Added") 
        db.session.commit()
        return jsonify("Creator Successfully Registered")

class AdminAPI(Resource):
    @roles_required('admin')
    @auth_token_required
    @cache.cached(timeout=50)
    def get(self, id=None):
        admin = user_datastore.find_user(id=id)
        print(admin.roles)
        if admin:
            admin_json = {
                'id': admin.id,
                'username': admin.username,
                'email': admin.email,
            }
            return jsonify(admin_json)
        else:
            return jsonify(message="User not found"), 404
    
class LogoutAPI(Resource):
    @auth_token_required
    @cache.cached(timeout=50)
    def post(self):
        return jsonify(message="Logged out")

class SongAPI(Resource):
    @cache.cached(timeout=50)
    def get(self, song_id=None):
        if song_id is None:
           songs = Song.query.all()
        else:
           songs = Song.query.filter(Song.song_id == song_id).all()

        if not songs:
            return jsonify({'message': 'No songs found'}), 404
        song_list = []
        for song in songs:
            song_json = {
                'id': song.song_id,
                'genre':song.genre,
                'name': song.song_name,
                'artist': song.artist,
                'release': song.release,
                'image': song.image,
                'audio':song.audio,
                'lyrics':song.lyrics
            }
    
            song_list.append(song_json)
        return jsonify(song_list)
    
    @roles_required('creator')
    def post(self,album_id):
        album=Album.query.filter(Album.album_id == album_id).first()
        name = request.form.get('song_name')
        print(name)
        artist=request.form.get('artist')
        genre=request.form.get('genre')
        release=request.form.get('release')
        print(release)
        if release:
            try:
                release = datetime.strptime(release, '%Y-%m-%d').date()
            except ValueError:
                print('error')
                return jsonify({'message': 'Invalid datetime format'}), 400
        image_file = request.files['image']
        audio_file = request.files['audio']
        img_file = secure_filename(image_file.filename)
        print(img_file)
        if image_file:
            image_file.save(os.path.join('templates/src/assets/images', img_file))
        aud_file = secure_filename(audio_file.filename)
        if audio_file:
            audio_file.save(os.path.join('templates/src/assets/audios', aud_file))
        lyrics = request.form.get('lyrics')
        music = Song(song_name=name, genre=genre, artist=artist, release=release, image=img_file, audio=aud_file, lyrics=lyrics,album_id=album_id)
        db.session.add(music)
        album.songs.append(music)
        db.session.commit()
        return jsonify({"message":"Song successfully added"})
    
    @roles_required('creator')
    def put(self,album_id,song_id):
        song=Song.query.filter(Song.song_id == song_id).first()
        name = request.form.get('song_name')
        print(name)
        artist=request.form.get('artist')
        genre=request.form.get('genre')
        release=request.form.get('release')
        print(release)
        if release:
            try:
                release = datetime.strptime(release, '%Y-%m-%d').date()
            except ValueError:
                print('error')
                return jsonify({'message': 'Invalid datetime format'}), 400
        image_file = request.files['image']
        audio_file = request.files['audio']
        img_file = secure_filename(image_file.filename)
        print(img_file)
        if image_file:
            image_file.save(os.path.join('templates/src/assets/images', img_file))
        aud_file = secure_filename(audio_file.filename)
        if audio_file:
            audio_file.save(os.path.join('templates/src/assets/audios', aud_file))
        lyrics = request.form.get('lyrics')
        try:
            song.image=img_file
            song.audio=aud_file
            song.release=release
            song.artist=artist
            song.genre=genre
            song.name=name
        except:
            return {'message': 'An error occurred while updating the song'}, 500
        db.session.commit()
        return jsonify({"message":"Song successfully added"})

    @roles_required('creator','admin')
    def delete(self, song_id):
        song=Song.query.filter(Song.song_id == song_id).first()
        if song is None:
            return jsonify({"message":"Song not found"}),404
        db.session.delete(song)
        db.session.commit()
        return "", 200

class AlbumAPI(Resource):
    @cache.cached(timeout=50)
    def get(self, album_id=None):
        if album_id is None:
           albums = Album.query.all()
        else:
           albums = Album.query.filter(Album.album_id == album_id).all()

        if not albums:
            return jsonify({'message': 'No albums found'}), 404
        album_list = []
        for album in albums:
            album_json = {
                'id': album.album_id,
                'name': album.name,
                'language': album.language,
                'artist': album.artist,
                'songs':[]
            }
            if album.songs:
                for songs in album.songs:
                    song_json={
                        'id': songs.song_id,
                        'name': songs.song_name,
                         'genre': songs.genre,
                        'artist': songs.artist,
                        'release': songs.release, 
                        'image':songs.image,
                        'audio':songs.audio,
                        'lyrics':songs.lyrics,
                    }
                    album_json['songs'].append(song_json)
            album_list.append(album_json)
        return jsonify(album_list)
    
    @roles_required('creator')
    def post(self):
        data=request.get_json()
        name = data.get('album_name')
        print(name)
        artist = data.get('artist')
        language = data.get('language')
        sho = Album(name=name, artist=artist, language=language)
        try:
            db.session.add(sho)
            db.session.commit()
        except:
            return jsonify({'message': 'An error occurred while adding the album'})
        return jsonify({"message":"Album successfully created"})

    @roles_required('creator')
    def put(self, album_id):
        album = Album.query.filter(Album.album_id == album_id).first()
        data=request.get_json()
        name = data.get('album_name')
        print(name)
        artist = data.get('artist')
        language = data.get('language')
        try:
            album.name = name
            album.artist = artist
            album.language = language
            db.session.commit()
        except:
            return {'message': 'An error occurred while updating the album'}, 500
        return jsonify({"message":"Album successfully updated"})

    

    @roles_required('creator','admin')
    def delete(self, album_id):
        album = Album.query.filter(Album.album_id == album_id).first()
        if album is None:
            return jsonify({"message":"Album not found"}),404
        for sh in album.songs:
            for songs in sh:
                db.session.delete(songs)
            db.session.commit()
        db.session.delete(album)
        db.session.commit()
        return "", 200

class PlaylistAPI(Resource):
    @cache.cached(timeout=50)
    def get(self, playlist_id=None):
        if playlist_id is None:
            playlists = Playlist.query.all()
        else:
            playlists = Playlist.query.filter(Playlist.playlist_id == playlist_id).all()

        if not playlists:
            return jsonify({'message': 'No playlists found'}), 404
        
        playlist_list = []
        for playlist in playlists:
            playlist_json = {
                'id': playlist.playlist_id,
                'name': playlist.name,
                'songs': []
            }
            for song in playlist.songs:
                song_json = {
                    'song_id': song.song_id,
                    'song_name': song.song_name,
                    'genre': song.genre,
                    'artist': song.artist,
                    'release': song.release.isoformat() if song.release else None,
                    'image': song.image,
                    'audio': song.audio,
                    'lyrics': song.lyrics
                }
                playlist_json['songs'].append(song_json)
            playlist_list.append(playlist_json)
        
        return jsonify(playlist_list)
    
    @roles_required('user')
    def post(self,user_id):
        user=User.query.filter(User.id == user_id).first()
        data=request.get_json()
        name = data.get('name')
        selected_songs = data.get('selected_songs')
        playlist = Playlist(name=name, user_id=user_id)  # Assuming Playlist model has 'name' and 'user_id' fields
        db.session.add(playlist)
    
        for song_id in selected_songs:
            song = Song.query.filter(Song.song_id==song_id).first
            if song:
               playlist.songs.append(song) 
        print(name)
        db.session.commit()
        return jsonify({"message":"Song successfully added"})
    
    @roles_required('user')
    def put(self, playlist_id):
        playlist = Playlist.query.get(playlist_id)
        if not playlist:
            return jsonify({'message': 'Playlist not found'}), 404

        data = request.get_json()
        if 'name' in data:
            playlist.name = data['name']

        if 'selected_songs' in data:
            selected_song_ids = data['selected_songs']
            playlist.songs = Song.query.filter(Song.song_id.in_(selected_song_ids)).all()

        db.session.commit()
        return jsonify({'message': 'Playlist updated successfully', 'playlist_id': playlist_id})
    
    def delete(self, playlist_id):
        playlist = Playlist.query.get(playlist_id)
        if not playlist:
            return jsonify({'message': 'Playlist not found'}), 404

        db.session.delete(playlist)
        db.session.commit()
        return jsonify({'message': 'Playlist deleted successfully', 'playlist_id': playlist_id})
    
class SearchAPI(Resource):
    @auth_token_required
    @roles_required('user')
    def post(self):
        data = request.get_json()
        query = data.get('query')
        id = None
        isname = None

        if query is not None:
            query_string = f"%{query}%"

            song_results = Song.query.filter(
                (Song.song_name.ilike(query_string)) |
                (Song.artist.ilike(query_string))
            ).all()
            album_results = Album.query.filter(
                (Album.name.ilike(query_string)) |
                (Album.artist.ilike(query_string))
            ).all()

            if album_results:
                isname = album_results[0].name
                id = album_results[0].album_id
            elif song_results:
                isname = song_results[0].song_name
                id = song_results[0].song_id

        return jsonify({"name": isname, "id": id, "message": "Search is successful"})

class RatingAPI(Resource):
    def post(self, id, song_id):
        data = request.get_json()
        rating = data.get('rating')
        print(rating)
        user = User.query.filter(User.id == id).first()
        song = Song.query.filter(Song.song_id == song_id).first()
        if not user or not song:
            return jsonify({'message': 'User or Song not found'}), 404
        user_rating = UserRating.query.filter_by(user_id=user.id, song_id=song.song_id).first()
        if user_rating:
            user_rating.rating = rating
        else:
            user_rating = UserRating(user_id=user.id, song_id=song.song_id, rating=rating)
            db.session.add(user_rating)
        
        db.session.commit()
        average_rating = db.session.query(func.avg(UserRating.rating)).filter_by(song_id=song.song_id).scalar()
        song.average_rating = average_rating
        db.session.commit()
        
        return jsonify({"message": 'Rating updated', "rating": rating, "average_rating": average_rating})



api.add_resource(RatingAPI,'/api/post/<int:id>/<int:song_id>/rating')
api.add_resource(SearchAPI,'/api/search')
api.add_resource(PlaylistAPI,'/api/get/playlist','/api/<int:user_id>/post/playlist','/api/delete/<int:playlist_id>/playlist')
api.add_resource(AlbumAPI,'/api/get/album','/api/post/album','/api/put/<int:album_id>/album','/api/delete/<int:album_id>/album')
api.add_resource(SongAPI,'/api/get/song','/api/<int:song_id>/get/song','/api/<int:album_id>/post/song','/api/<int:album_id>/<int:song_id>/put/song','/api/<int:song_id>/delete/song')
api.add_resource(UserAPI, '/api/<int:id>/user','/api/user')
api.add_resource(CreatorAPI, '/api/<int:id>/creator','/api/creator')
api.add_resource(AdminAPI,'/api/<int:id>/admin')
api.add_resource(AdminLoginAPI,'/api/admin/login')
api.add_resource(UserLoginAPI,'/api/user/login')
api.add_resource(CreatorLoginAPI,'/api/creator/login')
api.add_resource(LogoutAPI,'/api/logout')

# with app.app_context():
#     admin_role = user_datastore.find_or_create_role(name='admin',description='admin has access')
#     password="griss"
#     user=user_datastore.create_user(
#         username="griss",
#         password= bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
#         email="griss.harris@gmail.com",
#         active=True,
#         report="",
#         roles=[admin_role],
#         is_admin=True
#         )
#     db.session.commit()


if __name__=='__main__':
    with app.app_context():    
        db.create_all()
        # celery = make_celery(app)
    app.run(debug=True)