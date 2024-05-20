using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ChatAppClient.MVVM.Core;
using ChatAppClient.Net;
using ChatAppClient.MVVM.Model;
using System.Collections.ObjectModel;
using System.Windows;

namespace ChatAppClient.MVVM.ViewModel
{
    internal class MainViewModel
    {
        public ObservableCollection<UserModel> Users { get; set; }
        public ObservableCollection<string> Messages { get; set; }

        public RelayCommand ConnectToServerCommand { get; set; }
        public RelayCommand SendMessageCommand { get; set; }

        public string UserName { get; set; }
        public string Message { get; set; }

        private Server _server;

        public MainViewModel()
        {
            Users = new ObservableCollection<UserModel>();
            Messages = new ObservableCollection<string>();

            UserName = "Victim";

            _server = new Server();
            // += attaching event handler
            _server.connectedEvent += UserConnected;
            _server.messageReceivedEvent += MessageReceived;
            _server.userDisconnectedEvent += RemoveUser;
            _server.ConnectToServer(UserName);
            //this.ConnectToServerCommand = new RelayCommand(
                    //obj => _server.ConnectToServer(UserName)
                    //,obj => !string.IsNullOrEmpty(UserName)
                //);
            this.SendMessageCommand = new RelayCommand(
                //obj => _server.ConnectToServer(UserName),
                obj => _server.SendMessageToServer(Message),
                obj => !string.IsNullOrEmpty(Message)
            );
        }

        // invoked whenever we receive packet with the currect operation code
        public void UserConnected()
        {
            //throw new NotImplementedException();
            var user = new UserModel
            {
                UserName = _server.PacketReader.ReadMessage(),
                UID = _server.PacketReader.ReadMessage()
            };

            // check on server also

            if (!Users.Any(x => x.UID == user.UID))
            {
                Application.Current.Dispatcher.Invoke(() => Users.Add(user));
            }
;
        }

        public void MessageReceived()
        {
            var message = _server.PacketReader.ReadMessage();
            Application.Current?.Dispatcher.Invoke(() => Messages.Add(message));
        }

        public void RemoveUser()
        {
            var uid = _server.PacketReader.ReadMessage();
            var user = Users.Where(user => user.UID == uid).FirstOrDefault();
            Application.Current?.Dispatcher.Invoke(() => Users.Remove(user));
        }
    }
}