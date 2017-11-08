from socket import AF_INET, SOCK_STREAM, socket
from os import getpid
import protocol
from time import sleep
import pickle
from GUI.EnterNicknameDialog import *
from GUI.Gameplay import *

HOST = '127.0.0.1'
PORT = 7789

class Client:
    def leave_session(self):
        pass





    def send_request(self, m):
        socket.sendall(m)
        rsp = socket.recv(10000)
        if rsp == protocol._ACK:
            return True
        elif rsp == protocol._RSP_SESSION_FULL:
            return False
        else:
            return pickle.loads(rsp)



    def update(self, user_action, current_session):
        user_action = user_action.split(' ')
        row = user_action[1]
        column = user_action[2]
        number = user_action[3]

        update_request = self.send_request(protocol._REQ_UPDATE_GAME + protocol._MSG_FIELD_SEP +
                                           row + protocol._MSG_FIELD_SEP + column + protocol._MSG_FIELD_SEP + number)

        if update_request.game_state != current_session.game_state:
            print 'correct'
        else:
            print 'incorrect'

        return update_request


    def create_session(self, game_name, max_num_players):
        new_session = self.send_request(protocol._REQ_CREATE_SESSION + protocol._MSG_FIELD_SEP +
                                        game_name + protocol._MSG_FIELD_SEP + max_num_players)

        return new_session


    def get_current_sessions(self):
        current_sessions = self.send_request(protocol._REQ_CURRENT_SESSIONS)
        print 'Currently availabel sessions are: '
        for session in current_sessions:
            print '------------------ SESSION ---------------------'
            print session.game_name
            print session.game_id
            print ' '.join([player.nickname for player in session.current_players])#session.current_players
            print session.max_num_of_players
            print '------------------ SESSION ---------------------'





    def nickname(self, n):
        self.send_request(protocol._REQ_NICKNAME + protocol._MSG_FIELD_SEP + n)
        return


    def connect(self):
        self.send_request(protocol._REQ_INITIAL_CONNECT)
        return

    def join_session(self, user_action):
        session_id = user_action.split(' ')[1]
        rsp = self.send_request(protocol._REQ_JOIN_SESSION + protocol._MSG_FIELD_SEP + session_id)
        if type(rsp) != bool:
            return rsp
        else:
            return 'session full'





    def process_response(self, m):
        pass

if __name__ == '__main__':

    client = Client()
    socket = socket(AF_INET, SOCK_STREAM)
    socket.connect((HOST, PORT))
    client.connect()
    while True:
        sleep(1)
        print "in while"
        user_action = raw_input('enter action preceded by -flag: ')
        try:
            gameplayGUI = None
            if user_action.startswith('-username'):
                e = EnterNicknameDialog()
                client.nickname(e.nickname)
                # nickname(user_action.split(' ')[1])
                print 'username created'
            elif user_action.startswith('-newsession'):
                #current_session = create_session('test_game', '5')
                user_input = user_action.split(' ')
                current_session = client.create_session(user_input[1], user_input[2])
                print 'new session created'
            elif user_action.startswith('-printsession'):
                for i in current_session.game_state:
                    print i
            elif user_action.startswith('-getsessions'):
                client.get_current_sessions()
            elif user_action.startswith('-startSession'):
                # TODO: client as a class or creating a thread for the GUI for updating
                gameplayGUI = Gameplay(current_session)
            elif user_action.startswith('-update'):
                current_session = client.update(user_action, current_session)
                # TODO: gameplayGUI.update(current_session)
            elif user_action.startswith('-solution'):
                inf = user_action.split(' ')
            elif user_action.startswith('-join'):
                rsp = client.join_session(user_action)
                if type(rsp) == str:
                    print rsp
                else:
                    current_session = rsp
            elif user_action.startswith(protocol._TERMINATOR):
                client.send_request(protocol._TERMINATOR)
                
        except KeyboardInterrupt as e:
            break
