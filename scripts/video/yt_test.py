"""유튜브 API 연결 시험: 3초짜리 검은 화면 영상을 '일부 공개'로 올리고, 어느 채널에 올라갔는지와 공개 상태를 출력한다."""
import json, os, subprocess, time, requests
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=1080x1920:d=3', '-f', 'lavfi', '-i',
                'anullsrc=r=44100:cl=mono', '-t', '3', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '/tmp/t.mp4'], check=True)
at = requests.post('https://oauth2.googleapis.com/token', data={'client_id': os.environ['YT_CLIENT_ID'], 'client_secret': os.environ['YT_CLIENT_SECRET'],
                   'refresh_token': os.environ['YT_REFRESH_TOKEN'], 'grant_type': 'refresh_token'}, timeout=30)
print('토큰', at.status_code, at.json().get('error', 'ok')); at.raise_for_status(); H = {'Authorization': 'Bearer ' + at.json()['access_token']}
meta = {'snippet': {'title': 'API 업로드 시험 (삭제 예정)', 'description': '자동 업로드 연결 시험', 'categoryId': '25'},
        'status': {'privacyStatus': 'unlisted', 'selfDeclaredMadeForKids': False, 'containsSyntheticMedia': True}}
r = requests.post('https://www.googleapis.com/upload/youtube/v3/videos?uploadType=multipart&part=snippet,status', headers=H,
                  files={'m': ('m', json.dumps(meta), 'application/json'), 'v': ('v', open('/tmp/t.mp4', 'rb'), 'video/mp4')}, timeout=120)
print('업로드', r.status_code)
j = r.json(); print(json.dumps({'id': j.get('id'), 'channelId': j.get('snippet', {}).get('channelId'), 'channelTitle': j.get('snippet', {}).get('channelTitle'),
                                'status': j.get('status'), 'error': j.get('error', {}).get('message')}, ensure_ascii=False, indent=1))
