import streamlit as st
import sqlite3 as sql

font_css = """
<style>
@import urlurl('https://cdn.jsdelivr.net/gh/projectnoonnu/2410-1@1.0/RiaSans-ExtraBold.woff2') format('woff2');
html, body, [class*="css"] {
    font-family: 'Ria';
}
</style>
"""

# Streamlit 앱에 CSS 적용
st.markdown(font_css, unsafe_allow_html=True)

# 텍스트 출력 테스트
st.write("안녕하세요! Streamlit에 한글 폰트가 적용되었습니다.")
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