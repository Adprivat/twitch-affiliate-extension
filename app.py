# app.py
from flask import Flask, request, send_from_directory
from flask_restful import Resource, Api
from models import get_affiliate, create_affiliate, update_affiliate, delete_affiliate

app = Flask(__name__, static_folder='static')
api = Api(app)

class Affiliate(Resource):
    def get(self, streamer_id):
        """
        GET /affiliate/<streamer_id>
        Retrieves affiliate data for the given streamer.
        If no custom videos are set, default videos are provided.
        """
        affiliate = get_affiliate(streamer_id)
        if affiliate:
            # Convert datetime fields to ISO strings
            if "created_at" in affiliate and affiliate["created_at"]:
                affiliate["created_at"] = affiliate["created_at"].isoformat()
            if "updated_at" in affiliate and affiliate["updated_at"]:
                affiliate["updated_at"] = affiliate["updated_at"].isoformat()
            # Fallback: use 3 default videos if no custom videos are provided
            if "videos" not in affiliate or not affiliate["videos"]:
                affiliate["videos"] = [
                    "/static/videos/default1.mp4",
                    "/static/videos/default2.mp4",
                    "/static/videos/default3.mp4"
                ]
            return affiliate, 200
        else:
            return {"message": "Affiliate data not found"}, 404

    def put(self, streamer_id):
        data = request.get_json()
        if not data or 'affiliate_url' not in data:
            return {"message": "Missing affiliate_url in request"}, 400
        modified_count = update_affiliate(streamer_id, data['affiliate_url'])
        if modified_count:
            return {"message": "Affiliate updated successfully"}, 200
        else:
            return {"message": "No affiliate data updated"}, 404

    def delete(self, streamer_id):
        deleted_count = delete_affiliate(streamer_id)
        if deleted_count:
            return {"message": "Affiliate deleted successfully"}, 200
        else:
            return {"message": "Affiliate data not found"}, 404

class AffiliateList(Resource):
    def post(self):
        data = request.get_json()
        if not data or 'streamer_id' not in data or 'affiliate_url' not in data:
            return {"message": "Missing required data (streamer_id and affiliate_url)"}, 400
        affiliate_id = create_affiliate(data)
        return {"message": "Affiliate created successfully", "affiliate_id": str(affiliate_id)}, 201

# API-Routen registrieren
api.add_resource(Affiliate, '/affiliate/<string:streamer_id>')
api.add_resource(AffiliateList, '/affiliate')

# Route für die Startseite (kann als Landing-Page dienen)
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Route für das Panel (Live-Extension)
@app.route('/panel')
def serve_panel():
    return send_from_directory(app.static_folder, 'panel.html')

# Route für die Admin-Seite (Konfiguration)
@app.route('/admin')
def serve_admin():
    return send_from_directory(app.static_folder, 'admin.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
