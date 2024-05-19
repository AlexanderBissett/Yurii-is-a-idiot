// See https://aka.ms/new-console-template for more information


using System;
using System.Net;
using System.Net.Sockets;
using System.Collections.Generic;
using ChatAppServer.Net.IO;
using System.Linq;


namespace ChatAppServer
{
    internal class Program
    {
        static List<Client> _users;
        static TcpListener? _listener;

        static void Main(string[] args)
        {
            _users = new List<Client>();
            // 7891
            _listener = new TcpListener(IPAddress.Parse("93.93.112.211"), 87);
            _listener.Start();

            while (true)
            {
                var client = new Client(_listener.AcceptTcpClient());
                _users.Add(client);

                // Broadcast it to everyone on the server
                BroadcastConnection();
            }
        }

        static void BroadcastConnection()
        {

            foreach (var userReceiver in _users)
            {
                foreach (var userSender in _users)
                {
                    var broadcastPacket = new PacketBuilder();
                    broadcastPacket.WriteOperationCode(1);
                    broadcastPacket.WriteMessage(userSender.UserName);
                    broadcastPacket.WriteMessage(userSender.UID.ToString());

                    userReceiver.ClientSocket.Client.Send(broadcastPacket.GetPacketBytes());
                }
                //BroadcasMessage($"[{userReceiver.UserName}] connected");
            }
        }

        public static void BroadcasMessage(string message)
        {

            foreach (var user in _users)
            {

                var messagePacket = new PacketBuilder();
                messagePacket.WriteOperationCode(5);
                messagePacket.WriteMessage(message);

                user.ClientSocket.Client.Send(messagePacket.GetPacketBytes());

            }
        }

        public static void BroadcasDisconnect(string uid)
        {
            var disconnectUser = _users.Where(user => user.UID.ToString() == uid).FirstOrDefault();
            _users.Remove(disconnectUser);
            foreach (var user in _users)
            {
                var broadcastPacket = new PacketBuilder();
                broadcastPacket.WriteOperationCode(10);
                broadcastPacket.WriteMessage(uid);

                user.ClientSocket.Client.Send(broadcastPacket.GetPacketBytes());
            }
            BroadcasMessage($"[{disconnectUser.UserName}] disconnected");
        }
    }
}