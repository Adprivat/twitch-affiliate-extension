# app.py
import os
import requests
from flask import Flask, request, send_from_directory, jsonify
from flask_restful import Resource, Api
from models import get_affiliate, create_affiliate, update_affiliate, delete_affiliate

app = Flask(__name__, static_folder='static')
api = Api(app)

def require_twitch_oauth(func):
    """
    OAuth-Decorator:
    - Erwartet im Authorization-Header einen gültigen Bearer-Token.
    - Validiert diesen Token über Twitchs /validate-Endpoint.
    - Vergleicht die zurückgelieferte Twitch User ID mit der im URL-Pfad übergebenen streamer_id.
    Gibt im Fehlerfall ein Tuple (Dictionary, Statuscode) zurück.
    """
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return {"message": "Missing Authorization header"}, 401
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return {"message": "Invalid Authorization header format"}, 401
        token = parts[1]
        
        validate_url = "https://id.twitch.tv/oauth2/validate"
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(validate_url, headers=headers)
            if response.status_code != 200:
                return {"message": "Invalid token"}, 401
            token_info = response.json()
        except Exception as e:
            return {"message": "Error validating token", "error": str(e)}, 500
        
        twitch_user_id = token_info.get("user_id")
        if not twitch_user_id:
            return {"message": "Token validation did not return user_id"}, 401
        
        # Vergleiche den authentifizierten Twitch User mit der übergebenen streamer_id
        streamer_id = kwargs.get("streamer_id")
        if streamer_id and twitch_user_id != streamer_id:
            return {"message": "Forbidden: You can only access your own data."}, 403
        
        request.twitch_user_id = twitch_user_id
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

class Affiliate(Resource):
    @require_twitch_oauth
    def get(self, streamer_id):
        """GET /affiliate/<streamer_id>: Liefert Affiliate-Daten für den angegebenen Streamer."""
        affiliate = get_affiliate(streamer_id)
        if affiliate:
            if "created_at" in affiliate and affiliate["created_at"]:
                affiliate["created_at"] = affiliate["created_at"].isoformat()
            if "updated_at" in affiliate and affiliate["updated_at"]:
                affiliate["updated_at"] = affiliate["updated_at"].isoformat()
            if "videos" not in affiliate or not affiliate["videos"]:
                affiliate["videos"] = [
                    "/static/videos/default1.mp4",
                    "/static/videos/default2.mp4",
                    "/static/videos/default3.mp4"
                ]
            return affiliate, 200
        else:
            return {"message": "Affiliate data not found"}, 404

    @require_twitch_oauth
    def put(self, streamer_id):
        data = request.get_json()
        if not data or 'affiliate_url' not in data:
            return {"message": "Missing affiliate_url in request"}, 400
        modified_count = update_affiliate(streamer_id, data['affiliate_url'])
        if modified_count:
            return {"message": "Affiliate updated successfully"}, 200
        else:
            return {"message": "No affiliate data updated"}, 404

    @require_twitch_oauth
    def delete(self, streamer_id):
        deleted_count = delete_affiliate(streamer_id)
        if deleted_count:
            return {"message": "Affiliate deleted successfully"}, 200
        else:
            return {"message": "Affiliate data not found"}, 404

class AffiliateList(Resource):
    @require_twitch_oauth
    def post(self):
        data = request.get_json()
        if not data or 'streamer_id' not in data or 'affiliate_url' not in data:
            return {"message": "Missing required data (streamer_id and affiliate_url)"}, 400
        try:
            affiliate_id = create_affiliate(data)
            return {"message": "Affiliate created successfully", "affiliate_id": str(affiliate_id)}, 201
        except Exception as e:
            print("Error in POST /affiliate:", e)
            return {"message": "Internal server error: " + str(e)}, 500

api.add_resource(Affiliate, '/affiliate/<string:streamer_id>')
api.add_resource(AffiliateList, '/affiliate')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/panel')
def serve_panel():
    return send_from_directory(app.static_folder, 'panel.html')

@app.route('/admin')
def serve_admin():
    return send_from_directory(app.static_folder, 'admin.html')

@app.after_request
def remove_x_frame_options(response):
    # Entferne den X-Frame-Options-Header, damit Twitch die Seite in einem IFrame laden kann.
    response.headers.pop("X-Frame-Options", None)
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
