import matplotlib.pyplot as plt
from matplotlib import rc
import streamlit as st
import sqlite3 as sql
import matplotlib.font_manager as fm
import socket, time
font_css = """
<style>
@import url('https://jsdelivr.net');

html, body, [class*="st-"] {
    font-family: 'Pretendard';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/pretendard@1.0/Pretendard-Thin.woff2') format('woff2');
    font-weight: 100;
    font-display: swap;
}
</style>
"""
st.markdown(font_css, unsafe_allow_html=True)
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

def Connect_Event_Server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 613))  # 서버 주소와 포트 번호를 지정
        return s
    except Exception as e:
        print(f"서버 연결 실패: {e}")
        return None
def Change_Display(Where, PH, Users, Server613):
    st.session_state.show_content = False
    if Where == "Main":
        with PH.container():
            st.title("마피아 게임")
            Login_B = st.button('로그인', 2, on_click=lambda: Change_Display("Login", PH, Users, Server613))
            Code_B = st.button('관리자 코드 입력')
        return PH
    elif Where == "Login":
        with PH.container():
            st.title("로그인")
            ID = st.text_input("아이디")
            PW = st.text_input("비밀번호", type="password")
            Login_B1 = st.button('로그인', 1, on_click=lambda: LoginB(PH, Server613, Users))
        return PH
    elif Where == "Admin":
        with PH.container():
            st.title("관리자 모드")
            Admin_Code = st.text_input("관리자 코드 입력", type="password")
            if Admin_Code == "admin140827Roymin":
                st.success("관리자 코드 인증 성공")
                Amount = int(st.text_input("인원 수"))
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM).bind(('', 613))
                server.listen(Amount)
            else:
                st.error("관리자 코드 인증 실패")
        return PH
    st.session_state.show_content = False
def LoginB(place_holder, Server613, Users):
    st.write("로그인 버튼 클릭됨") 
    [ID, PW, Login_B] = Change_Display("Login", place_holder)
    if Login_B:
        if Server613 and ID in [user.ID for user in Users] and PW == [user.PW for user in Users if user.ID == ID][0]:
            st.success("로그인 성공")
            LoginSuccessed = True
        else:
            st.error("로그인 실패")
            LoginSuccessed = False
        Server613.sendto(f"LOGIN|{ID}|{PW}|{LoginSuccessed}".encode(), ("localhost", 613))
def AdminB():
    Admin_Code = st.text_input("관리자 코드 입력", type="password")
    if Admin_Code == "admin140827Roymin":  # 예시로 관리자 코드를 "admin123"으로 설정
        st.success("관리자 코드 인증 성공")
        Amount = int(st.text_input("인원 수"))
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM).bind(('', 613))  # 관리자 서버에 연결
        server.listen(Amount)
    else:
        st.error("관리자 코드 인증 실패")
def runApp(Debug, Users, Roles, Missions):
    # 시스템 폰트 사용 (나눔고딕 또는 기본 폰트)
    rc('font', family='RiaSans-ExtraBold')
    place_holder = st.empty()
    plt.rcParams['axes.unicode_minus'] = False
    st.write(Debug)
    Server613 = Connect_Event_Server()
    place_holder = Change_Display("Main", place_holder, Users, Server613)
Running = False
if __name__ == "__main__":
    if Running ==  False:
        Running = True
        Users = Load_Users_Data()
        Roles = Load_Role()
        Missions = Load_Missions()
        runApp("진행중인 이벤트가 없습니다.", Users, Roles, Missions)
        try:
            while True:
                time.sleep(1)
        except RuntimeError:
            pass
"""
613: 전체 서버
6131: 팀 1 서버
6132: 팀 2 서버
6130: 관리자 서버

"""