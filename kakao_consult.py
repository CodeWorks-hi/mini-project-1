import streamlit as st

# 본인의 카카오톡 채널 ID 입력
channel_public_id = "_xfxhjXn"  # 올바른 채널 ID 반영

# 카카오톡 버튼 HTML & JavaScript 코드
channel_public_id = "_xfxhjXn"
kakao_buttons = f"""
<style>
.kakao-buttons-container {{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 15px;
    margin-top: 20px;
    z-index: 1000;
}}

.kakao-button {{
    flex: 0 1 auto;
}}
</style>

<div class="kakao-buttons-container">
    <div id="kakao-talk-channel-add-button" class="kakao-button"
         data-channel-public-id="{channel_public_id}"
         data-size="large"
         data-support-multiple-densities="true"></div>

    <div id="kakao-talk-channel-chat-button" class="kakao-button"
         data-channel-public-id="{channel_public_id}"
         data-title="consult"
         data-size="large"
         data-color="yellow"
         data-shape="pc"
         data-support-multiple-densities="true"></div>
</div>

<script>
  window.kakaoAsyncInit = function() {{
    Kakao.Channel.createAddChannelButton({{
      container: '#kakao-talk-channel-add-button'
    }});
    Kakao.Channel.createChatButton({{
      container: '#kakao-talk-channel-chat-button'
    }});
  }};

  (function(d, s, id) {{
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = 'https://t1.kakaocdn.net/kakao_js_sdk/2.7.4/kakao.channel.min.js';
    js.integrity = 'sha384-8oNFBbAHWVovcMLgR+mLbxqwoucixezSAzniBcjnEoumhfIbMIg4DrVsoiPEtlnt';
    js.crossOrigin = 'anonymous';
    fjs.parentNode.insertBefore(js, fjs);
  }})(document, 'script', 'kakao-js-sdk');
</script>
"""

# 사이드바에 카카오톡 버튼 적용
with st.sidebar:
    st.components.v1.html(kakao_buttons, height=100)