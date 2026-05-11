import re
import html as _html

MAX_ACTION_LENGTH = 500
MAX_SETUP_LENGTH = 1000


def sanitize_user_input(text: str, max_length: int = MAX_ACTION_LENGTH) -> str:
    if not isinstance(text, str):
        return ""
    text = text[:max_length]
    text = text.strip()
    # 줄바꿈·탭은 허용, 나머지 제어 문자 제거
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return text


def safe_html(text: str) -> str:
    """일반 텍스트를 HTML에 안전하게 삽입할 수 있도록 이스케이프한다. 줄바꿈은 <br>로 변환."""
    return _html.escape(str(text)).replace('\n', '<br>')
