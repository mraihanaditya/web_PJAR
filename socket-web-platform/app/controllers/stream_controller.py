from flask import Blueprint, Response, session, request
import socket
import re
from config import Config
from app.models.video import Video

stream_bp = Blueprint('stream', __name__)

@stream_bp.route('/video/<video_id>')
def stream_video(video_id):
    if not session.get('logged_in'):
        return "Unauthorized", 401
        
    # 1. Cari metadata video di Database
    video = Video.query.get_or_404(video_id)
    
    # 2. Baca rentang byte (Range) yang diminta HTML5 Video Player
    range_header = request.headers.get('Range', None)
    byte1, byte2 = 0, None
    if range_header:
        match = re.search(r'bytes=(\d+)-(\d*)', range_header)
        groups = match.groups()
        if groups[0]: byte1 = int(groups[0])
        if groups[1]: byte2 = int(groups[1])
        
    # Minta potongan maksimal 60KB per request UDP
    chunk_size = 1024 * 60 
    length = chunk_size
    
    # 3. Kirim perintah UDP ke server
    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_client.settimeout(2.0)
    command = f"FETCH|{video.filename}|{byte1}|{length}".encode('utf-8')
    
    try:
        udp_client.sendto(command, (Config.UDP_SERVER_IP, Config.UDP_SERVER_PORT))
        chunk, _ = udp_client.recvfrom(65536)
    except socket.timeout:
        return "Timeout dari UDP Server", 500
    finally:
        udp_client.close()
        
    if chunk == b"ERROR_NOT_FOUND":
        return "File tidak ditemukan di server", 404

    # 4. Kembalikan data UDP ke Browser menggunakan standar HTTP 206
    resp = Response(chunk, 206, mimetype='video/mp4', content_type='video/mp4', direct_passthrough=True)
    resp.headers.add('Content-Range', f'bytes {byte1}-{byte1 + len(chunk) - 1}/{video.size}')
    resp.headers.add('Accept-Ranges', 'bytes')
    
    return resp