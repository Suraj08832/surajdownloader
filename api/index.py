from flask import Flask, jsonify, request, Response
import yt_dlp
import os
import tempfile

app = Flask(__name__)
app.json.sort_keys = False

FAVICON_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="#ff0000"/><polygon points="40,25 40,75 75,50" fill="white"/></svg>'''

COOKIES_CONTENT = """# Netscape HTTP Cookie File
.youtube.com	TRUE	/	TRUE	1770704847	LOGIN_INFO	AFmmF2swRQIgNGkDUBtCGpbyrghQT0tWFpfMQPS9KCEUpPODMlPNIWwCIQC2CBWceu81MCBsWB4Baw1pf3SqA_5D22GW3jbouhSGZA:QUQ3MjNmemtob3JkZ05YZ2lrUGpIbVBwRXk2ZHFrb0VtRzdIZ2tmaHFqeUZBeGxBdko5MzZvT0lCWXZkbFZwd0RyNkVqb1d6WVVkb0sxdFRUWEZhX0h2dTlfUHlXN2hkVElINzdhMEk2TUNGWnNMNDdCRnQ5WGU5ZWZXazhwOUJTMHpQYmVkRmpacy1UTk0yc2xtZFRBUGFCM2JTNi1hSzZB
.youtube.com	TRUE	/	TRUE	1781114771	PREF	f4=4000000&tz=Asia.Calcutta&f7=100
.youtube.com	TRUE	/	FALSE	1779360012	SID	g.a0003wjx1OxwERsi_jbYPTIgq4HWJZWqSvbIgLzwU6GALLBWI7sOIV4WHWrMyrhBGGVIaxPaqQACgYKAWISARESFQHGX2MiAhyUvJjR4x9yVvq6Nj9D2BoVAUF8yKqnAtflZguLc0drrBiCNZD-0076
.youtube.com	TRUE	/	TRUE	1779360012	__Secure-1PSID	g.a0003wjx1OxwERsi_jbYPTIgq4HWJZWqSvbIgLzwU6GALLBWI7sO1aXec3YHL17L_XxHS8KFeQACgYKAUASARESFQHGX2Mi2NGsBkJi3Nk2Yi1rfEHh8BoVAUF8yKot0caG26LpEjagNX1V6mjD0076
.youtube.com	TRUE	/	TRUE	1779360012	__Secure-3PSID	g.a0003wjx1OxwERsi_jbYPTIgq4HWJZWqSvbIgLzwU6GALLBWI7sO4-dinAqQInep8HXKTn1RrAACgYKASMSARESFQHGX2MiBRQO7NU5IsFh3ibcSGMBGRoVAUF8yKp5SyVc86pe_33LJF1xDdmU0076
.youtube.com	TRUE	/	FALSE	1779360012	HSID	AZ6Ss-N5G7ikI8GJG
.youtube.com	TRUE	/	TRUE	1779360012	SSID	ANr7N4jTducFotrlc
.youtube.com	TRUE	/	FALSE	1779360012	APISID	E8SWJGBv2CN8NCd7/AWI75uMLfeTuF5AO3
.youtube.com	TRUE	/	TRUE	1779360012	SAPISID	BSwotq3K_osWdRba/AJ07-3YcjI9m_ZicB
.youtube.com	TRUE	/	TRUE	1779360012	__Secure-1PAPISID	BSwotq3K_osWdRba/AJ07-3YcjI9m_ZicB
.youtube.com	TRUE	/	TRUE	1779360012	__Secure-3PAPISID	BSwotq3K_osWdRba/AJ07-3YcjI9m_ZicB
.youtube.com	TRUE	/	TRUE	0	wide	1
.youtube.com	TRUE	/	TRUE	1781120175	__Secure-1PSIDTS	sidts-CjQBflaCdbZ5G7h-waRVXqQeITFrr0VRSX77vUdXFpZNHN3uUXKqDMndS7Af5elUCNVfTAf-EAA
.youtube.com	TRUE	/	TRUE	1781120175	__Secure-3PSIDTS	sidts-CjQBflaCdbZ5G7h-waRVXqQeITFrr0VRSX77vUdXFpZNHN3uUXKqDMndS7Af5elUCNVfTAf-EAA
.youtube.com	TRUE	/	FALSE	1781120175	SIDCC	AKEyXzWDL9-SA-VbdlXmRhLnJ__rnMu_b5qrtmuz339I-4yTsoBeRD-gnlBAPgnCTVslQ2eiZ_c
.youtube.com	TRUE	/	TRUE	1781120175	__Secure-1PSIDCC	AKEyXzU-vkYDWRUm2bf5jLk6mDnO_Pvmw9e5NXk67c92Q1TW3zb-wsCJ5caatVUbtKkWpqWcjQ
.youtube.com	TRUE	/	TRUE	1781120175	__Secure-3PSIDCC	AKEyXzV74LJSxZ_LXjegb_fC48lGkCZHsOtivdPsQXfpSjbiQBn5TAD0Ndwx5WLrk-1nNfrNZpg
.youtube.com	TRUE	/	TRUE	1781114748	VISITOR_INFO1_LIVE	bm_Jiq98kyw
.youtube.com	TRUE	/	TRUE	1781114748	VISITOR_PRIVACY_METADATA	CgJJThIEGgAgTA%3D%3D
.youtube.com	TRUE	/	TRUE	1781095671	__Secure-ROLLOUT_TOKEN	CO_2k4e6_-LopgEQ6dPNo5bzigMYs4y024q4kQM%3D
.youtube.com	TRUE	/	TRUE	0	YSC	dNHArf9jhzw
"""

def get_cookies_file():
    tmp_cookies = os.path.join(tempfile.gettempdir(), 'yt_cookies.txt')
    with open(tmp_cookies, 'w') as f:
        f.write(COOKIES_CONTENT)
    return tmp_cookies

@app.route('/favicon.ico')
@app.route('/favicon.png')
def favicon():
    return Response(FAVICON_SVG, mimetype='image/svg+xml')

def get_ydl_opts(extract_flat=False):
    opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': extract_flat,
        'skip_download': True,
        'ignoreerrors': True,
        'cookiefile': get_cookies_file(),
    }
    return opts

def success_response(data):
    return jsonify({"success": True, "data": data})

def error_response(message, status_code=400):
    return jsonify({"success": False, "message": message}), status_code

def format_thumbnail(thumbnails):
    if not thumbnails:
        return []
    if isinstance(thumbnails, list):
        return [{"url": t.get("url"), "width": t.get("width"), "height": t.get("height")} for t in thumbnails if t.get("url")]
    return []

def extract_video_info(info):
    formats = info.get("formats", [])
    audio_formats = []
    for fmt in formats:
        if fmt.get("acodec") != "none" and fmt.get("vcodec") == "none":
            audio_formats.append({
                "quality": f"{fmt.get('abr', 0)}kbps" if fmt.get('abr') else fmt.get('format_note', 'unknown'),
                "url": fmt.get("url"),
                "format": fmt.get("ext", "m4a"),
                "filesize": fmt.get("filesize") or fmt.get("filesize_approx"),
                "acodec": fmt.get("acodec"),
                "itag": fmt.get("format_id")
            })
    audio_formats.sort(key=lambda x: float(x['quality'].replace('kbps', '').replace('unknown', '0') or 0))
    
    return {
        "id": info.get("id"),
        "name": info.get("title"),
        "type": "song",
        "duration_seconds": info.get("duration"),
        "channelId": info.get("channel_id"),
        "viewCount": info.get("view_count"),
        "author": info.get("uploader") or info.get("channel"),
        "image": format_thumbnail(info.get("thumbnails")),
        "description": info.get("description"),
        "uploadDate": info.get("upload_date"),
        "downloadUrl": audio_formats
    }

@app.route('/')
def index():
    return success_response({
        "name": "YouTube Music API (yt-dlp)",
        "version": "2.0.0",
        "description": "YouTube Music API powered by yt-dlp",
        "endpoints": {
            "search": {
                "all": {"method": "GET", "path": "/api/search", "params": ["q", "limit"]},
            },
            "songs": {
                "get": {"method": "GET", "path": "/api/songs/<id>", "description": "Get song details with download URLs"},
                "download": {"method": "GET", "path": "/api/songs/<id>/download", "description": "Get download URLs only"},
            },
            "playlists": {
                "get": {"method": "GET", "path": "/api/playlists/<id>"}
            }
        }
    })

@app.route('/api/search')
def search_all():
    query = request.args.get('q', '')
    limit = request.args.get('limit', 20, type=int)
    
    if not query:
        return error_response("Missing 'q' query parameter")
    
    try:
        ydl_opts = get_ydl_opts(extract_flat=True)
        ydl_opts['playlistend'] = limit
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_url = f"ytsearch{limit}:{query}"
            result = ydl.extract_info(search_url, download=False)
            
            entries = result.get("entries", [])
            formatted = []
            for item in entries:
                if item:
                    formatted.append({
                        "id": item.get("id"),
                        "name": item.get("title"),
                        "type": "video",
                        "duration_seconds": item.get("duration"),
                        "author": item.get("uploader") or item.get("channel"),
                        "viewCount": item.get("view_count"),
                        "image": format_thumbnail(item.get("thumbnails"))
                    })
            
            return success_response({
                "query": query,
                "total": len(formatted),
                "results": formatted
            })
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/api/songs/<video_id>')
def get_song(video_id):
    try:
        ydl_opts = get_ydl_opts()
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            url = f"https://music.youtube.com/watch?v={video_id}"
            info = ydl.extract_info(url, download=False)
            
            if not info:
                return error_response("Video not found", 404)
            
            result = extract_video_info(info)
            return success_response(result)
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/api/songs/<video_id>/download')
def get_song_download(video_id):
    try:
        ydl_opts = get_ydl_opts()
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            url = f"https://music.youtube.com/watch?v={video_id}"
            info = ydl.extract_info(url, download=False)
            
            if not info:
                return error_response("Video not found", 404)
            
            formats = info.get("formats", [])
            audio_formats = []
            for fmt in formats:
                if fmt.get("acodec") != "none" and fmt.get("vcodec") == "none":
                    audio_formats.append({
                        "quality": f"{fmt.get('abr', 0)}kbps" if fmt.get('abr') else fmt.get('format_note', 'unknown'),
                        "url": fmt.get("url"),
                        "format": fmt.get("ext", "m4a"),
                        "filesize": fmt.get("filesize") or fmt.get("filesize_approx"),
                        "acodec": fmt.get("acodec"),
                        "itag": fmt.get("format_id")
                    })
            
            if not audio_formats:
                return error_response("No audio formats available", 404)
            
            audio_formats.sort(key=lambda x: float(x['quality'].replace('kbps', '').replace('unknown', '0') or 0))
            
            return success_response({
                "id": video_id,
                "downloadUrl": audio_formats
            })
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/api/playlists/<playlist_id>')
def get_playlist(playlist_id):
    try:
        ydl_opts = get_ydl_opts(extract_flat=True)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            url = f"https://music.youtube.com/playlist?list={playlist_id}"
            info = ydl.extract_info(url, download=False)
            
            if not info:
                return error_response("Playlist not found", 404)
            
            entries = info.get("entries", [])
            tracks = []
            for item in entries:
                if item:
                    tracks.append({
                        "id": item.get("id"),
                        "name": item.get("title"),
                        "type": "song",
                        "duration_seconds": item.get("duration"),
                        "author": item.get("uploader") or item.get("channel"),
                        "image": format_thumbnail(item.get("thumbnails"))
                    })
            
            result = {
                "id": playlist_id,
                "name": info.get("title"),
                "type": "playlist",
                "description": info.get("description"),
                "trackCount": len(tracks),
                "author": info.get("uploader") or info.get("channel"),
                "image": format_thumbnail(info.get("thumbnails")),
                "tracks": tracks
            }
            
            return success_response(result)
    except Exception as e:
        return error_response(str(e), 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
