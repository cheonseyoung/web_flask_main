from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/')
def test():
    return render_template('index.html')


@app.route('/calculate',methods=['POST'])
def cal():
    if request.method=='POST':

        ## SKT_MPP_ENGINE_REST에서 가져온 부

        SOCKET_DATA_ENDIAN = 'little'
        SOCKET_DATA_LENGTH_LEN = 4
        SOCKET_DATA_DECODE_TYPE = 'UTF-8'

        def _get_bytes_stream(sock, length):
            """
            소켓에서 주어진 길이만큼 데이터를 수신
            주어진 길이만큼 데이터를 한번에 수신하지 못한 경우에는,
            해당 길이 만큼 데이터를 수신할 때까지 소켓에서 데이터를 읽는다.

            :param sock: 소켓 객체
            :param length: 수신할 데이터 길이
            :return: 수신한 데이터
            """
            buf = b''
            try:
                step = length
                while True:
                    data = sock.recv(step)
                    buf += data
                    if len(buf) == length:
                        break
                    elif len(buf) < length:
                        step = length - len(buf)
            except InterruptedError as e:
                raise Exception(e)

            return buf[:length]

        def send_data(socket, data):
            """
            소켓을 이용한 데이터 전송
            전송할 데이터의 길이를 먼저 전송한 다음,
            실제 보낼 데이터를 전송한다.
            sendall(모든 데이터가 전송되거나 에러가 발생할 때까지 date를 계속 전송)

            :param socket: 소켓 객체
            :param data: 전송할 데이터
            :return:
            """
            try:
                message = json.dumps(data)

                # length
                length = len(message)
                socket.sendall(length.to_bytes(SOCKET_DATA_LENGTH_LEN, byteorder=SOCKET_DATA_ENDIAN))

                # data
                socket.sendall(message.encode())
            except Exception as e:
                raise Exception(e)

        def receive_data(socket):
            """
            소켓에서 데이터를 수신
            데이터 길이(SOCKET_DATA_LENGTH_LEN)를 먼저 수신한 다음,
            실제 데이터를 수신한다.

            :param socket:
            :return: 수신한 데이터
            """
            try:
                # length
                data = socket.recv(SOCKET_DATA_LENGTH_LEN)
                length = int.from_bytes(data, SOCKET_DATA_ENDIAN)

                # data
                data = _get_bytes_stream(socket, length)
                if not data:
                    return None
                decode_data = json.loads(data.decode(SOCKET_DATA_DECODE_TYPE))
                return decode_data
            except Exception as e:
                raise Exception(e)

    return render_template('info.html')

if __name__=='__main__':
    app.run()