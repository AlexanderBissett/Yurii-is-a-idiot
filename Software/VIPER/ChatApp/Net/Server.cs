using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;
using ChatAppClient.Net.IO;

namespace ChatAppClient.Net
{
    class Server
    {
        TcpClient _client;
        //PacketBuilder _packetBuilder;
        public PacketReader PacketReader;

        public event Action connectedEvent;
        public event Action messageReceivedEvent;
        public event Action userDisconnectedEvent;

        public Server()
        {
            _client = new TcpClient();
        }

        public void ConnectToServer(string username)
        {
            if (!_client.Connected)
            {
                // put here local address and a free port
                _client.Connect("93.93.112.211", 87);
                // if we get a connection, not in constructor
                PacketReader = new PacketReader(_client.GetStream());

                if (!string.IsNullOrEmpty(username))
                {
                    var connectPacket = new PacketBuilder();
                    connectPacket.WriteOperationCode(0);
                    connectPacket.WriteMessage(username);
                    _client.Client.Send(connectPacket.GetPacketBytes());
                }

                ReadPackets();
;           }
        }

        public void ReadPackets()
        {
            // new thread, in future keep thack of it
            Task.Run(() =>
            {
                while (true)
                {
                    // maybe make ReadOperation that reads and returns byte from a stream
                    var operationCode = PacketReader.ReadByte();
                    switch (operationCode)
                    {
                        // case 0: handled in different place
                        case 1:
                            connectedEvent?.Invoke();
                            break;
                        case 5:
                            messageReceivedEvent?.Invoke();
                            break;
                        case 10:
                            userDisconnectedEvent?.Invoke();
                            break;
                        default:
                            System.Console.WriteLine("Default case");
                            break;
                    }
                }
            });
        }

        public void SendMessageToServer(string message)
        {
            var messagePacket = new PacketBuilder();
            messagePacket.WriteOperationCode(5);
            messagePacket.WriteMessage(message);

            _client.Client.Send(messagePacket.GetPacketBytes());
        }
    }
}
