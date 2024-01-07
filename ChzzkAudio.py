import streamlit as st
import requests
import m3u8
import json

content = None
channelImageWidth = 120

def get_stream_url(username='룩삼오피셜'):
    global content
    req_result = requests.get(f"https://api.chzzk.naver.com/service/v1/search/channels?keyword={username}")
    try:
        channelId = req_result.json()['content']['data'][0]['channel']['channelId']
        if channelId:
            content = requests.get(f"https://api.chzzk.naver.com/service/v2/channels/{channelId}/live-detail").json()['content']
            return content
    except:
        st.error(f'{username}을 찾지 못했습니다.')
        return False

st.title("Chzzk Audio Finder")
username = st.text_input("Enter Chzzk username:", value='룩삼오피셜', placeholder='치지직 닉네임')

if username:
    try:
        if get_stream_url(username):
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
                stream_url_low = playlists.media[1].base_uri + playlists.media[1].uri
                stream_url_high = playlists.media[0].base_uri + playlists.media[0].uri
                
                st.success(f"Stream found")
                st.image(content['channel']['channelImageUrl'], width = channelImageWidth)
                st.write(f"닉네임: {real_username}")
                st.write(f"제목: {title}")
                st.write(f"카테고리: {liveCategoryValue}({liveCategory})")
                st.write(f'Low(AAC 64kbps): {stream_url_low}')
                st.write(f'High(AAC 192kbps): {stream_url_high}')
                st.write("둘 중 하나를 복사하여 플레이어(VLC, 팟플레이어 등)로 재생하세요.")
            else:
                status_message = 'close'
                st.error(f'\'{real_username}\'은(는) 방송 중이 아닙니다.')
                st.image(content['channel']['channelImageUrl'], width = channelImageWidth)
        else:
            st.error(f'{username}을 찾지 못했습니다.')
    except Exception as e:
        st.write(e)

    try:
        if content and live_status == "OPEN" and userAdultStatus == "NOT_LOGIN_USER":
            st.error("성인인증이 필요한 방송입니다. 오디오 주소를 받아올 수 없습니다.")
            st.image(content['channel']['channelImageUrl'], width = channelImageWidth)
            st.write(f"닉네임: {real_username}")
            st.write(f"제목: {title}")
            st.write(f"카테고리: {liveCategoryValue}({liveCategory})")
    except Exception as e:
        st.write(e)
else:
    st.write("닉네임 입력 대기 중")
