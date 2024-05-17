using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;
using ChatAppServer.Net.IO;

namespace ChatAppServer
{
    internal class Client
    {
        public string UserName { get; set; }
        public Guid UID { get; set; }
        public TcpClient ClientSocket { get; set; }

        PacketReader _packetReader;

        public Client(TcpClient client)
        {
            ClientSocket = client;
            // .ToString() at any time
            UID = Guid.NewGuid();
            _packetReader = new PacketReader(ClientSocket.GetStream());

            byte operationCode = _packetReader.ReadByte();
            // if operationCode!=0 drop connection
            UserName = _packetReader.ReadMessage();

            DateTime dt = DateTime.Now;
            //string timeStamp = $"{dt.Date} {dt.Hour}:{dt.Minute}";
            //DateTime secondsStripped = dt.Date.AddHours(dt.Hour).AddMinutes(dt.Minute);
            Console.WriteLine($"[{dt}] : Client \"{UserName}\" has connected");
            //Program.BroadcasMessage($"[{dt}]: \"{UserName}\" has connected");

            Task.Run(() => Process());
        }

        void Process()
        {
            while (true)
            {
                try
                {
                    var operationCode = _packetReader.ReadByte();
                    switch (operationCode)
                    {
                        case 5:
                            var message = _packetReader.ReadMessage();
                            DateTime dt = DateTime.Now;
                            //string timeStamp = $"{dt.Date} {dt.Hour}:{dt.Minute}";
                            //DateTime secondsStripped = dt.Date.AddHours(dt.Hour).AddMinutes(dt.Minute);
                            Console.WriteLine($"[{dt}]: Message received {message}");
                            Program.BroadcasMessage($"[{dt}]: [{UserName}]: {message}");
                            break;
                        default:
                            break;
                    }
                }
                catch (Exception)
                {
                    //Console.WriteLine($"[{DateTime.Now}: {UID} disconnected");
                    //Program.BroadcasDisconnect(UID.ToString());
                    DateTime dt = DateTime.Now;
                    //string timeStamp = $"{dt.Date} {dt.Hour}:{dt.Minute}";
                    //DateTime secondsStripped = dt.Date.AddHours(dt.Hour).AddMinutes(dt.Minute);
                    Console.WriteLine($"[{dt}: \"{UserName}\" disconnected");
                    Program.BroadcasDisconnect(UID.ToString());
                    ClientSocket.Close();
                    break;
                    //throw;
                }
            }
        }
    }
}
