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
    def __init__(self, ID, PW, Name, Level, Exp, Team):
        self.ID = ID
        self.PW = PW
        self.Name = Name
        self.Level = Level
        self.Exp = Exp
        self.Team = Team
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
    def __init__(self, User: User, Role, NickName, Team, Votes, Missions, Status, X, Y):
        self.User = User
        self.Role = Role
        self.NickName = NickName
        self.Team = Team
        self.Votes = Votes
        self.Missions = Missions
        self.Status = Status
        self.X = X
        self.Y = Y
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
    data = [id, password, name, level, exp, team]
    return User(data[0], data[1], data[2], data[3], data[4], data[5])
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
class Display:
    def __init__(self, Buttons, texts, Titles, name, game):
        self.buttons = Buttons
        self.texts = texts
        self.titles = Titles
        self.name = name
        self.game = game
Button_Key = {"Main": {"Login": [0], "Admin": [0]}, "Login": {"Login2": [0]}, "Admin": {"Admin2": [0]}}
Input_Key = {"Main": {}, "Login": {"ID": [0], "PW": [0]}, "Admin": {"Admin_Code": [0], "Amount": [0]}}
admin_code = ["admin140827Roymin", "admin14????SongZung", "admin14????Cherry"]
admin_name = ['류민', '정우', '채원']
def Make_Button(Label):
    global Max_Id
    if "Max_Id" not in st.session_state:
        st.session_state["Max_Id"] = 0
    try:
        st.session_state["Max_Id"] += 1
        return st.button(Label, key=st.session_state["Max_Id"])
    except:
        return st.button("오류")
def Make_Text_Input(Label):
    global Max_Id
    if "Max_Id" not in st.session_state:
        st.session_state["Max_Id"] = 0
    try:
        st.session_state["Max_Id"] += 1
        return st.text_input(Label, key=st.session_state["Max_Id"])
    except:
        return st.text_input("오류")
Id = -1
def Change_Display(Where, Users, Server613):
    st.session_state["display"] = Where
    if st.session_state["display"] == "Admin" or Where == "Admin":
            st.title("관리자 모드")
            Admin_Code = st.text_input("관리자 코드 입력", key="Admin_Code_Admin")
            inzung = st.button("인증", key="Admin_Admin")
            if Admin_Code in admin_code and inzung:
                st.success(f"관리자 코드 인증 성공! ({admin_name[admin_code.index(Admin_Code)]}으로 인증됨)")
                Amount = st.text_input("인원 수", key="Amount_Admin")
                if admin_name[admin_code.index(Admin_Code)] == '류민':
                    serverPort = 6131
                else:
                    serverPort = 6132
                if st.button("이벤트 서버 생성"):
                    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM).bind(('', serverPort))
                    server.listen(Amount)
            elif not Admin_Code in admin_code and inzung:
                st.error("관리자 코드 인증 실패")
    elif st.session_state["display"] == "Login" or Where == "Login":
            st.title("로그인")
            PW = st.text_input("로그인 코드", key="Login_PW")
            if st.button("로그인", key="Login_Login"):
                LoginB(Server613, Users, PW)
    elif st.session_state["display"] == "WaitRoom" or Where == "WaitRoom":
        st.title("대기실")
        st.write("대기실에 입장하셨습니다. 게임이 시작될 때까지 기다려주세요.")
        st.write("게임이 시작되면 자동으로 게임 화면으로 전환됩니다.")
        L = [user for user in Users]
        S = ''
        for i in range(len(L)-1):
            if L[i].Team != Users[Id].Team:
                S += f"{L[i].Name}, "
        st.write(f"당신은 {S[0:-3]}와 같은 조입니다")
    else:
            st.title("마피아 게임")
            if st.button("로그인", key="Login_Main"):
                st.session_state["display"] = "Login"
                st.rerun()
            if st.button("관리자 코드 입력", key="Admin_Main"):
                st.session_state["display"] = "Admin"
                st.rerun()
def LoginB(Server613, Users, PW):
    if PW in [user.PW for user in Users]:
        st.success("로그인 성공")
        LoginSuccessed = True
        Id = -([user.PW for user in Users].index(PW)-1)
        st.session_state["display"] = "WaitRoom"
        st.rerun()
    else:
        st.error("로그인 실패")
        LoginSuccessed = False
    try:
        Server613.sendto(f"LOGIN|{PW}|{LoginSuccessed}".encode(), ("localhost", 613))
    except:
        pass
def AdminB():
    Admin_Code = Make_Text_Input("관리자 코드 입력")
    {Button_Key['Admin']['Admin2'].append(Button_Key['Admin']['Admin2'][-1]+1) if Button_Key['Admin']['Admin2'] else Button_Key['Admin']['Admin2'].append(0)}
    if Admin_Code in admin_code:  # 예시로 관리자 코드를 "admin123"으로 설정
        st.success(f"관리자 코드 인증 성공! ({admin_name[admin_code.index(Admin_Code)]}으로 인증됨)")
        Amount = int(Make_Text_Input("인원 수"))
        if admin_name[admin_code.index(Admin_Code)] == '류민':
            serverPort = 6131
        else:
            serverPort = 6132
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM).bind(('', serverPort))  # 관리자 서버에 연결
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

    if "display" not in st.session_state:
        st.session_state["display"] = "Main"

    Change_Display(st.session_state["display"], Users, Server613)
if __name__ == "__main__":
    if "ReS" not in st.session_state:
        st.session_state["ReS"] = False
    if "Max_Id" not in st.session_state:
        st.session_state["Max_Id"] = 0
    if not st.session_state["ReS"] or True:
        st.session_state["ReS"] = True
        Userss = Load_Users_Data()
        Users = []
        for i in range(len(Userss)):
            Users.append(User_Data_Conv_to_Class(Userss[i]))
            print(Users[-1])
        Roles = Load_Role()
        Missions = Load_Missions()
        runApp("진행중인 이벤트가 없습니다.", Users, Roles, Missions)