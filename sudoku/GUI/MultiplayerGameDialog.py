from Tkinter import *
import tkMessageBox


class MultiplayerGameDialog:
    def __init__(self, client):
        self.root = Tk()
        self.client = client
        self.session = None     # either filled with the create_session or join_session
        self.lblName = Label(self.root, text="Name: ")
        self.lblName.grid(row=0)
        self.enterName = Entry(self.root)
        self.enterName.grid(row=0, column=1)
        self.lblNumber = Label(self.root, text="Number of Players: ")
        self.lblNumber.grid(row=0, column=2)
        self.enterNumber = Entry(self.root)
        self.enterNumber.grid(row=0, column=3)
        self.btnCreateNewSession = Button(self.root, text="create", command=self.create_session)
        self.btnCreateNewSession.grid(row=0, column=4)
        self.listSessions = Listbox(self.root)
        self.listSessions.bind("<Double-Button-1>", self.select_session_from_list_on_double_click)
        self.listSessions.grid(row=1, columnspan=4)
        # Done: request sessions from server
        self.currentSessions = self.get_current_sessions(self.client)
        for item in self.currentSessions:
            self.listSessions.insert(END, item.game_name)
        self.root.mainloop()

    def create_session(self):
        self.name = self.enterName.get()
        self.number = self.enterNumber.get()
        self.session = self.client.create_session(self.name, self.number)
        self.root.destroy()

    def select_session_from_list_on_double_click(self, event):
        index = event.widget.curselection()[0]
        self.currentSession = self.currentSessions[index]
        rsp = self.client.join_session(self.currentSession.game_id)
        if type(rsp) == str:
            tkMessageBox.showinfo('Session is full!', 'Oops.. people already having fun on this session. try another!')
        else:
            self.session = rsp
            self.root.destroy()


    def get_current_sessions(self,client):
        return client.get_current_sessions()