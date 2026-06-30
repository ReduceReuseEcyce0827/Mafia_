import streamlit as st
import sqlite3 as sql

import base64



# 1. 로컬 폰트 파일을 읽어서 Base64로 인코딩하는 함수
def get_base64_font(font_path):
    with open(font_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


# 2. 폰트 파일 경로 설정 (예시: 눈누에서 다운로드한 TTF 파일)
font_file_path = "RiaSans-ExtraBold.ttf"

try:
    # 3. Base64 문자열 생성
    base64_font = get_base64_font(font_file_path)

    # 4. CSS 작성 및 적용
    font_css = f"""
    <style>
    @font-face {{
        font-family: 'CustomFont';
        src: url(data:font/ttf;base64,{base64_font}) format('truetype');
    }}

    html, body, [class*="css"] {{
        font-family: 'CustomFont', sans-serif;
    }}
    </style>
    """
    st.markdown(font_css, unsafe_allow_html=True)

except FileNotFoundError:
    st.error(
        f"폰트 파일을 찾을 수 없습니다. 경로를 확인해주세요: {font_file_path}"
    )

# 5. 결과 확인
st.title("Base64 한글 폰트 적용 완료")
st.write("인터넷 연결 없이도 이 한글 폰트가 올바르게 표시됩니다.")
# Streamlit 앱에 CSS 적용
"""
class User: #게임 종류 후에도 유지될 영구적인 데이터 e
    def __init__(self, ID, PW, Name, Level, Exp):
        self.ID = ID
        self.PW = PW
        self.Name = Name
        self.Level = Level
        self.Exp = Exp
    def __str__(self):
        return f"ID: {self.ID}, Password: {self.PW}, Name: {self.Name}, Level: {self.Level}, Exp: {self.Exp}"
class Game:
    def __init__(self, id, time):
        self.Id = id
        self.Time = time
class Mission: #시민은 모든 미션을 완료하면 승리
    def __init__(self, ID, Text, Location, Description):
        self.ID = ID
        self.Text = Text
        self.Location = Location
        self.Description = Description
    def __str__(self):
        return f"ID: {self.ID}, Name: {self.Text}, Location: {self.Location}, Description: {self.Description}"
class Role: #직업
    def __init__(self, ID, Name, is_neutral, Description):
        self.ID = ID
        self.Name = Name
        self.is_neutral = is_neutral
        self.Description = Description
    def __str__(self):
        return f"ID: {self.ID}, Name: {self.Name}, is_neutral: {self.is_neutral}, Description: {self.Description}"
class Player: #게임 진행 시 만들어지는 일시적인 데이터
    def __init__(self, User: User, Role, NickName, Team, Votes, Missions, Status):
        self.User = User
        self.Role = Role
        self.NickName = NickName
        self.Team = Team
        self.Votes = Votes
        self.Missions = Missions
        self.Status = Status
    def __str__(self):
        return f"User: [{self.User}], Role: {self.Role}, NickName: {self.NickName}, Team: {self.Team}, Votes: {self.Votes}, Missions: {self.Missions}, Status: {self.Status}"
def Reset_Tables():
    conn = sql.connect("Mafia.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions")
    conn.commit()
    conn.close()
def Load_DB(Table: str):
    conn = sql.connect("Mafia.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {Table}")
    return cursor.fetchall()
def Load_Users_Data():
    return Load_DB("players")
def Load_Missions():
    return Load_DB("missions")
def Load_Role():
    return Load_DB("roles")
def User_Data_Conv_to_Class(User_Data):
    (name, id, level, role_id, mission_id, status, vote_count, team, password, exp) = User_Data
    data = [id, password, name, level, exp]
    return User(data[0], data[1], data[2], data[3], data[4])
def Mission_Data_Conv_to_Class(Mission):
    (Id, Name, isNeutral, Desc) = Mission
    data = [Id, Name, isNeutral, Desc]
    return Role(data[0], data[1], data[2], data[3])
def Role_Data_Conv_to_Class(Role):
    (Id, Name, isNeutral, Desc) = Role
    data = [Id, Name, isNeutral, Desc]
    return Role(data[0], data[1], data[2], data[3])


def runApp(Debug):
    rc('font', family='RiaSans-ExtraBold')
    plt.rcParams['axe.unicode_minus'] = False
    st.title("D-0613 Laboratory Sinario Carbon Copy: Doppelganger Escape")
    Start_B = st.button('게임 시작')
    st.write(Debug)
Reset_Tables()
Users = []
for i in range(27):
    Users.append(User_Data_Conv_to_Class(Load_Users_Data()[i]))
Missions = []
for i in range(17):
    Users.append(User_Data_Conv_to_Class(Load_Users_Data()[i]))
Roles = []
for i in range(25):
    Users.append(User_Data_Conv_to_Class(Load_Users_Data()[i]))
"""