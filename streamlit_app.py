import matplotlib.pyplot as plt
from matplotlib import rc
import streamlit as st
import sqlite3 as sql
import matplotlib.font_manager as fm
import socket, time, threading, random
import streamlit.components.v1 as components
from PIL import Image
if __name__ == "__main__":
    if not "team1C" in st.session_state:
        st.session_state["team1C"] = []
    if not "team2C" in st.session_state:
        st.session_state["team2C"] = []
    if not "ServerT1" in st.session_state:
        st.session_state["ServerT1"] = []
    if not "ServerT2" in st.session_state:
        st.session_state["ServerT2"] = []
    if not "ServerMT" in st.session_state:
        st.session_state["ServerMT"] = []
    if not "ServerClient" in st.session_state:
        st.session_state["ServerClient"] = []
    if not "display" in st.session_state:
        st.session_state["display"] = "Main"
    if not "Job" in st.session_state:
        st.session_state["Job"] = ""
    if not "PL" in st.session_state:
        st.session_state["PL"] = []
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
        self.Data = []
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
    def __init__(self, User: User, Role, NickName, Team, Votes, Missions, Status, X, Y, Color):
        self.User = User
        self.Role = Role
        self.NickName = NickName
        self.Team = Team
        self.Votes = Votes
        self.Missions = Missions
        self.Status = Status
        self.X = X
        self.Y = Y
        self.Color = Color
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
def Role_Data_Conv_to_Class(Rolee):
    (Id, Name, isNeutral, Desc) = Rolee
    data = [Id, Name, isNeutral, Desc]
    return Role(data[0], data[1], data[2], data[3])

def Connect_Event_Server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, 613))  # 서버 주소와 포트 번호를 지정
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
class Game_UI:
    def __init__(self, Mission, Chatting, JobIcon, AbilityIcon):
        self.Mission = Mission
        self.Chatting = Chatting
        self.JobIcon = JobIcon
        self.AbilityIcon = AbilityIcon


Button_Key = {"Main": {"Login": [0], "Admin": [0]}, "Login": {"Login2": [0]}, "Admin": {"Admin2": [0]}}
Input_Key = {"Main": {}, "Login": {"ID": [0], "PW": [0]}, "Admin": {"Admin_Code": [0], "Amount": [0]}}
admin_code = ["admin140827Roymin", "admin140618SongZung", "admin14????Cherry"]
admin_name = ['류민', '정우', '채원']
def A():
    while True:
        st.session_state["ServerT1"][-1].settimeout(10000000)
def B():
    while True:
        st.session_state["ServerT2"][-1].settimeout(10000000)
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
server = None
query_params = st.query_params
def Wait():
    try:
        client_socket, addr = st.session_state["ServerT1"][-1].accept()
        st.session_state["team1C"].append(client_socket)
        st.write(f"연결 수락됨: {addr}")
        client_socket.send("Hello!".encode('utf-8'))
    except socket.timeout:
        st.write("타임아웃!")
def Wait2():
    try:
        client_socket, addr = st.session_state["ServerT2"][-1].accept()
        st.session_state["team2C"].append(client_socket)
        st.write(f"연결 수락됨: {addr}")
        client_socket.send("Hello!".encode('utf-8'))
    except socket.timeout:
        st.write("타임아웃!")
def Get1():
    try:
        while True:
            for t1 in range(len(st.session_state["team1C"])):
                try:
                    st.write(st.session_state["team1C"][t1].recv(1024).decode('utf-8'))
                except Exception as e:
                    st.write(e)
            st.write("1")
    except RuntimeError:
        pass
def Get2():
    try:
        while True:
            for t2 in range(len(st.session_state["team2C"])):
                try:
                    st.write(st.session_state["team2C"][t2].recv(1024).decode('utf-8'))
                except:
                    pass
            st.write("2")
    except RuntimeError:
        pass
def Get3():
    try:
        while True:
            for t1 in range(len(st.session_state["ServerMT"])):
                try:
                    st.write(st.session_state["ServerMT"][t1].recv(1024).decode('utf-8'))
                except Exception as e:
                    st.write(e)
            st.write("1")
    except RuntimeError:
        pass
wait1 = threading.Thread(target=Wait)
wait2 = threading.Thread(target=Wait2)
get1 = threading.Thread(target=Get1)
get2 = threading.Thread(target=Get2)
get3 = threading.Thread(target=Get3)
settimeout = threading.Thread(target=A)
host = "0.0.0.0"
def Get_InGame_Admin():
    Player_Data = {"Team": [t.team for t in Users],
                   "Name": [t.Name for t in Users],
                   "Id": [t.Id for t in Users]}
    try:
            while True:
                try:
                    for i in range(len(st.session_state["ServerMT"])):
                        data = st.session_state["ServerMT"][i].recv(1024).decode('utf-8')
                        Data_L = data.split('|')
                        if "위치" == Data_L[0]:
                            Team = Player_Data["Name"].index(Data_L[1])
                            st.session_state[f"ServerT{Team}"][i].sendall(f"위치|{Data_L[1]}|{Data_L[2]}")
                            pass
                        if "미션완료" == Data_L[0]:
                            # 미션 완료시 실행되는 메커니즘
                            pass
                        if "상태변경" == Data_L[0]:
                            # 상태 변경시 실행되는 메커니즘
                            pass
                        if "회의" == Data_L[0]:
                            # 회의 시작시 실행되는 메커니즘
                            pass
                        if "능력사용" == Data_L[0]:
                            # 능력 사용시 실행되는 메커니즘
                            pass
                        if "채팅" == Data_L[0]:
                            # 채팅시 실행되는 메커니즘
                            pass
                except TimeoutError:
                    pass
                except Exception as e:
                    st.write(e)
    except Exception as e:
            st.write(e)
def Get_InGame_User():
    Player_Data = {"Team": [t.Team for t in Users],
                   "Name": [[t.Name for t in Users]],
                   "Id": [[t.Id for t in Users]]}
    try:
            while True:
                try:
                    for i in range(len(st.session_state["ServerMT"])):
                        data = st.session_state["ServerMT"][i].recv(1024).decode('utf-8')
                        Data_L = data.split('|')
                        if "플레이어위치" == Data_L[0]:
                            st.session_state["PL"].append(f"{Data_L[1]}|{Data_L[2]}")
                            # {f"{Data_L[1]}": f"{Data_L[2]}"}
                            pass
                        if "미션완료" == Data_L[0]:
                            # 미션 완료시 실행되는 메커니즘
                            pass
                        if "상태변경" == Data_L[0]:
                            # 상태 변경시 실행되는 메커니즘
                            pass
                        if "회의" == Data_L[0]:
                            # 회의 시작시 실행되는 메커니즘
                            pass
                        if "능력사용" == Data_L[0]:
                            # 능력 사용시 실행되는 메커니즘
                            pass
                        if "채팅" == Data_L[0]:
                            # 채팅시 실행되는 메커니즘
                            pass
                except TimeoutError:
                    pass
                except Exception as e:
                    st.write(e)
    except Exception as e:
            st.write(e)
Get_InGame = threading.Thread(target=Get_InGame_User)
def Debugging():
    pass
def Change_Display(Where, Users): 
    if st.session_state["display"] == "Admin":
            st.title("관리자 모드")
            Admin_Code = st.text_input("관리자 코드 입력", key="Admin_Code_Admin", type="password")
            inzung = st.button("인증", key="Admin_Admin")
            if Admin_Code in admin_code and inzung:
                st.success(f"관리자 코드 인증 성공! ({admin_name[admin_code.index(Admin_Code)]}으로 인증됨)")
                if Admin_Code == "admin140827Roymin":
                    try:
                        server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        server1.settimeout(5)
                        server1.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                        server1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        if hasattr(socket, 'SO_REUSEPORT'):
                            server1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                        server1.bind((host, 16131))
                        if not server1 in st.session_state["ServerT1"]:
                            st.session_state["ServerT1"].append(server1)
                            
                        server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        server2.settimeout(5)
                        server2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                        server2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        if hasattr(socket, 'SO_REUSEPORT'):
                            server2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                        server2.bind((host, 26132))
                        if not server2 in st.session_state["ServerT2"]:
                            st.session_state["ServerT2"].append(server2)

                        st.success("서버 생성됨")
                        st.session_state["display"] = "ControlCenter"
                        st.rerun()
                    except OSError as e:
                        st.write(e)
                else: 
                    server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server1.settimeout(5)
                    server1.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                    server1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    server1.connect((host, 16131))
                    st.session_state["ServerT1"].append(server1)
                    
                    server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server2.settimeout(5)
                    server2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                    server2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    server2.connect((host, 26132))
                    st.session_state["ServerT2"].append(server2)

                    st.success("서버 연결됨")
                    st.session_state["display"] = "ControlCenter"
                    st.rerun()
            elif not Admin_Code in admin_code and inzung:
                st.error("관리자 코드 인증 실패")
    elif st.session_state["display"] == "Login":
            st.title("로그인")
            PW = st.text_input("로그인 코드", key="Login_PW")
            if st.button("로그인", key="Login_Login"):
                LoginB(Users, PW)
    elif st.session_state["display"] == "WaitRoom" or Where == "WaitRoom":
        if Users[Id].Team == 1:
            serverPort = 16131
        else:
            serverPort = 26132
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.settimeout(5)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        server.connect((host, serverPort))
        st.session_state["ServerMT"].append(server)
        st.session_state["ServerMT"][-1].send(str(Users[Id].Name).encode('utf-8'))
        st.title("대기실")
        st.write("대기실에 입장하셨습니다. 게임이 시작될 때까지 기다려주세요.")
        st.write("게임이 시작되면 자동으로 게임 화면으로 전환됩니다.")
        if st.button("❤️"):
            st.session_state["ServerMT"][-1].send("Heart".encode('utf-8'))
        if st.button("😊"):
            st.session_state["ServerMT"][-1].send("Happy".encode('utf-8'))
        if st.button("😂"):
            st.session_state["ServerMT"][-1].send("Fun".encode('utf-8'))
        if st.button("👍"):
            st.session_state["ServerMT"][-1].send("Good".encode('utf-8'))
        L = [user for user in Users]
        S = ''
        for i in range(len(L)-1):
            if L[i].Team != Users[Id].Team:
                S += f"{L[i].Name}, "
        st.write(f"당신은 {S[0:-2]}와 같은 조입니다.")
        server = st.session_state["ServerMT"][-1]
        try:
            while True:
                try:
                    for i in range(len(st.session_state["ServerMT"])):
                        data = st.session_state["ServerMT"][i].recv(1024).decode('utf-8')
                        if "SG" == data[0:2]:
                            st.session_state["Job"] = data.split("|")[1]
                            st.session_state["display"] = "InGame"
                            st.rerun()
                            break
                        st.write(data)
                except TimeoutError:
                    pass
                except Exception as e:
                    st.write(e)
        except:
            pass
        st.rerun()
    elif st.session_state["display"] == "ControlCenter" or Where == "ControlCenter":
        st.title("컨트롤 센터")
        st.write("관리자만 사용할 수 있는 컨트롤 센터입니다.")
        Buttons = {"Start_T1": st.button('게임 시작', key="Team1S"),
                   "Test": st.button('메세지 보내기')}
        Inputs = {"Message": st.text_input('보낼 메세지', key="Message001")}
        Game_Status = ["Loading"]
        PL = []
        if True:
            st.session_state["ServerT1"][-1].listen(3)
            st.session_state["ServerT2"][-1].listen(3)
            L1 = []
            for i in range(len(Users)):
                L1.append(Users[i].PW)
            L2 = []
            for i in range(len(Users)):
                L2.append(Users[i].Data)
            L3 = []
            for i in range(len(Users)):
                L3.append(Users[i].Name)
            if Buttons["Start_T1"]:
                Game_Status.remove("Loading")
                Game_Status.append("Game")
                st.write(st.session_state["team1C"])
                st.write(st.session_state["team2C"])
                T1Job = [Roles[i].Name for i in range(len(Roles))]
                T2Job = T1Job
                for t1 in range(len(st.session_state["team1C"])):
                    st.session_state["team1C"][t1].send(f"SG|{T1Job.pop(random.randint(0, len(T1Job)-1))}".encode('utf-8'))
                    st.write("보냄")
                for t2 in range(len(st.session_state["team2C"])):
                    st.session_state["team2C"][t2].send(f"SG|{T2Job.pop(random.randint(0, len(T2Job)-1))}".encode('utf-8'))
                    st.write("보냄")
                Location = ["순간이동 장치실", "전기실", "창고", "온실", "옷장", "회의실", "연회실"]
                T1L = []
                T2L = []
                for t1 in range(len(st.session_state["team1C"])):
                    T1L.append(f"플레이어위치|{Users[L2.index(st.session_state["team1C"][t1])].Name}|{Location[random.randint(0, 6)]}")
                for t2 in range(len(st.session_state["team2C"])):
                    T2L.append(f"플레이어위치|{Users[L2.index(st.session_state["team2C"][t2])].Name}|{Location[random.randint(0, 6)]}")
                for t1 in range(len(st.session_state["team1C"])):
                    for i in range(len(T1L)):
                        st.session_state["team1C"][t1].send(T1L[i].encode('utf-8'))
                for t2 in range(len(st.session_state["team2C"])):
                    for i in range(len(T1L)):
                        st.session_state["team2C"][t2].send(T2L[i].encode('utf-8'))
            if Buttons["Test"]:
                st.write(st.session_state["team1C"])
                st.write(st.session_state["team2C"])
                for t1 in range(len(st.session_state["team1C"])):
                    st.session_state["team1C"][t1].send(Inputs["Message"].encode('utf-8'))
                    st.write("메세지 보냄")
                for t2 in range(len(st.session_state["team2C"])):
                    st.session_state["team2C"][t2].send(Inputs["Message"].encode('utf-8'))
                    st.write("메세지 보냄")
            try:
                while True:
                    client_socket, addr = st.session_state["ServerT1"][-1].accept()
                    st.session_state["team1C"].append(client_socket)
                    st.write(f"연결 수락됨: {addr}")
                    PL.append(st.session_state["team1C"][-1].recv(1024).decode('utf-8'))
                    Users[L3.index(PL[-1])].Data = addr
                    for i in range(len(st.session_state["team1C"])):
                        st.session_state["team1C"][i].send(f"{Users[L1.index(PW)].Name}님이 참여하셨습니다.".encode('utf-8'))
                    client_socket, addr = st.session_state["ServerT2"][-1].accept()
                    st.session_state["team2C"].append(client_socket)
                    st.write(f"연결 수락됨: {addr}")
                    PL.append(st.session_state["team2C"][-1].recv(1024).decode('utf-8'))
                    Users[L3.index(PL[-1])].Data = addr
                    for i in range(len(st.session_state["team2C"])):
                        st.session_state["team2C"][i].send(f"{Users[L1.index(PW)].Name}님이 참여하셨습니다.".encode('utf-8'))
            except:
                    pass
            try:
                while True:
                    
                    time.sleep(2)
            except:
                    pass
    elif st.session_state["display"] == "InGame" or Where == "InGame":
        st.title("인게임")
        st.write(st.session_state["Job"])
        Group = {"BackGroundIMG": st.image(st.session_state["BGIMG"], caption="배경")}
        #순간이동실, 전기실, 창고, 온실, 옷장, 회의실, 연회실
        Test_Button = {'Move': {"Teleporter": st.button("순간이동 장치실로 이동", key="Move001"),
                                "Electricity": st.button("전기실로 이동", key="Move002"),
                                "ChangGo": st.button("창고로 이동", key="Move003"),
                                "Farm": st.button("온실로 이동", key="Move004"),
                                "DressRoom": st.button("옷장으로 이동", key="Move005"),
                                "BoardRoom": st.button("회의실로 이동", key="Move006"),
                                "Hall": st.button("연회실로 이동", key="Move007")}}
        Getss = ""
        Get_InGame.start()
        if Test_Button["Move"]["Teleporter"]:
            Location = "순간이동 장치실"
        if Test_Button["Move"]["Electricity"]:
            Location = "전기실"
        if Test_Button["Move"]["ChangGo"]:
            Location = "창고"
        if Test_Button["Move"]["Farm"]:
            Location = "온실"
        if Test_Button["Move"]["DressRoom"]:
            Location = "옷장"
        if Test_Button["Move"]["BoardRoom"]:
            Location = "회의실"
        if Test_Button["Move"]["Hall"]:
            Location = "연회실"
        try:
            while True:
                for i in range(len(st.session_state["PL"])):
                    st.write(f"{st.session_state["PL"][i].split('|')[0]}의 위치: {st.session_state["PL"][i].split('|')[1]}")
                time.sleep(3)
        except RuntimeError:
            pass
    else:
            st.title("마피아 게임")
            if st.button("로그인", key="Login_Main"):
                st.session_state["display"] = "Login"
                st.rerun()
            if st.button("관리자 코드 입력", key="Admin_Main"):
                st.session_state["display"] = "Admin"
                st.rerun()
def LoginB(Users, PW):
    global Id
    if PW in [user.PW for user in Users]:
        st.success("로그인 성공")
        LoginSuccessed = True
        Id = int(-([user.PW for user in Users].index(PW)-1))
        st.session_state["display"] = "WaitRoom"
        st.rerun()
    else:
        st.error("로그인 실패")
        LoginSuccessed = False
def runApp(Debug, Users, Roles, Missions):
    # 시스템 폰트 사용 (나눔고딕 또는 기본 폰트)
    rc('font', family='RiaSans-ExtraBold')
    place_holder = st.empty()
    plt.rcParams['axes.unicode_minus'] = False
    st.write(Debug)

    Change_Display(st.session_state["display"], Users)
def Reload_STClose():
    if "refresh" in query_params:
        for i in range(len(st.session_state["ServerT1"])):
            st.session_state["ServerT1"][i].close()
        for i in range(len(st.session_state["ServerT2"])):
            st.session_state["ServerT2"][i].close()
        for i in range(len(st.session_state["ServerMT"])):
            st.session_state["ServerMT"][i].close()
if __name__ == "__main__":
    if not "refresh" in query_params:
            st.session_state["ReS"] = True
            Userss = Load_Users_Data()
            Users = []
            for i in range(len(Userss)):
                Users.append(User_Data_Conv_to_Class(Userss[i]))
            Roless = Load_Role()
            Roles = []
            for i in range(len(Roless)):
                Roles.append(Role_Data_Conv_to_Class(Roless[i]))
            Missions = Load_Missions()
            Reload_STClose()
            st.session_state["BGIMG"] = Image.open("Images/Background.png")
            runApp("진행중인 이벤트가 없습니다.", Users, Roles, Missions)
            