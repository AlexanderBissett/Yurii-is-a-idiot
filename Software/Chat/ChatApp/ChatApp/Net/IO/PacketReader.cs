using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Net.Sockets;

namespace ChatAppClient.Net.IO
{
    internal class PacketReader : BinaryReader
    {
        private NetworkStream _networkStream;

        public PacketReader(NetworkStream networkStream) : base(networkStream)
        {
            _networkStream = networkStream;
        }

        public string ReadMessage()
        {
            byte[] messageBuffer = null;
            var length = ReadInt32();
            messageBuffer = new byte[length];
            _networkStream.Read(messageBuffer, 0, length);

            var message = Encoding.ASCII.GetString(messageBuffer);
            return message;
        }
    }
}
