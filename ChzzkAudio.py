import streamlit as st
import requests
import m3u8
import json
live_status, real_username, liveCategoryValue, liveCategory, userAdultStatus = None, None, None, None, None
def get_stream_url(username='룩삼오피셜'):
    global real_username,liveCategoryValue, liveCategory, live_status
    req_result = requests.get(f"https://api.chzzk.naver.com/service/v1/search/channels?keyword={username}")
    channelId = req_result.json()['content']['data'][0]['channel']['channelId']
    if channelId:
        content = requests.get(f"https://api.chzzk.naver.com/service/v2/channels/{channelId}/live-detail").json()['content']
        real_username = content['channel']['channelName']
        title = content['liveTitle']
        liveCategoryValue = content['liveCategoryValue']
        liveCategory = content['liveCategory']
        live_status = content['status']
        userAdultStatus = content["userAdultStatus"]
        if live_status == "OPEN":
            status_message = 'open'
            video_m3u8 = json.loads(content['livePlaybackJson'])['media'][0]['path']
            playlists = m3u8.load(video_m3u8)
            return title, playlists.media[1].base_uri+playlists.media[1].uri, playlists.media[0].base_uri+playlists.media[0].uri
        else:
            status_message = 'close'
            st.error(f'\'{real_username}\'은(는) 방송 중이 아닙니다.')
    else:
        st.error(f'{username}을 찾지 못했습니다.')

st.title("Chzzk Audio Finder")
username = st.text_input("Enter Chzzk username:", value='룩삼오피셜', placeholder='치지직 닉네임')

if username:
    if live_status == "OPEN":
        try:
            title, stream_url_low, stream_url_high = get_stream_url(username)
            if stream_url_low and stream_url_high:
                st.success(f"Stream found")
                st.write(f"닉네임: {real_username}")
                st.write(f"제목: {title}")
                st.write(f"카테고리: {liveCategoryValue}({liveCategory})")
                st.write(f'Low(AAC 64kbps): {stream_url_low}')
                st.write(f'High(AAC 192kbps): {stream_url_high}')
                st.write("둘 중 하나를 복사하여 플레이어(VLC, 팟플레이어 등)로 재생하세요.")
            elif userAdultStatus == "NOT_LOGIN_USER":
                st.write(f"닉네임: {real_username}")
                st.write(f"제목: {title}")
                st.write(f"카테고리: {liveCategoryValue}({liveCategory})")
                st.write("성인인증이 필요한 방송입니다. 오디오 주소를 가져올 수 없습니다.")
            else:
                st.error("Stream not found.")
                st.write(status_message)
    except:
        pass
else:
    print("닉네임 입력 대기 중")
