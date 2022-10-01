import 'dart:io';
import 'package:flutter/material.dart';
import 'package:cp949/cp949.dart' as cp949;
import 'package:flutter_tts/flutter_tts.dart';
import 'package:provider/provider.dart';
import 'package:untitled/pages/first_page.dart';
import 'package:untitled/pages/provider/count_provider.dart';

void main() {
  return runApp(
      ChangeNotifierProvider(
        create: (BuildContext context)=> CountProvider(),
        child: MaterialApp(home: SocketClient(),),
      )
  );
}

late SocketClientState pageState;

class SocketClient extends StatefulWidget {//StatefulWidget
  @override                                     //1.생성자(Constructors)가 없는 경우 기본 생성자(default constructor,SocketClient();:생성자의 이름이 클래스와 동일하고 매개변수가 없는 생성자)가 자동으로 제공된다.
  SocketClientState createState() {             //2.state 생성, widget삭제
    pageState = SocketClientState();
    return pageState;
  }
}

class SocketClientState extends State<SocketClient> { //State class: 하위 클래스(SocketClientState)는 상위 클래스(SocketClient)의 생성자(SocketClient();)를 상속받지 않는다.
  FlutterTts flutterTts = FlutterTts();
  final scaffoldKey = GlobalKey<ScaffoldState>();
  late CountProvider _countProvider;

  String localIP = "192.203.145.56";
  int port = 50000;
  List<MessageItem> items = <MessageItem>[];

  Socket? clientSocket;
  String runstop="stop";
  String ocrrunstop="ocrstop";

  void connectToServer() async {
    Socket.connect(localIP, port, timeout: Duration(seconds: 2))
        .then((socket) {      //왼쪽.then().오른쪽 : 왼쪽 실행후 오른쪽
      setState(() {           //ui 안바꾸고 실행
        clientSocket = socket;
      });

      showSnackBarWithKey(
          "Connected to ${socket.remoteAddress.address}:${socket.remotePort}");
      initSetting();
      flutterTts.speak("연결되었습니다.");
      socket.listen(
            (onData) {
            var onnData = String.fromCharCodes(onData).trim();
            print(cp949.decodeString(onnData));
            initSetting();
            flutterTts.speak(cp949.decodeString(onnData));
            setState(() {
              items.insert(
                  0,
                  MessageItem(clientSocket!.remoteAddress.address,
                      cp949.decodeString(onnData))
              );
            });
        },

        onDone: onDone,
        onError: onError,
      );

    }).catchError((e) {
      showSnackBarWithKey(e.toString());
    });
  }


  @override
  Widget build(BuildContext context) {
    _countProvider=Provider.of<CountProvider>(context);
    return MaterialApp(
        title: '발곰이',
        theme: ThemeData(
          primarySwatch: Colors.amber,
        ),
        debugShowCheckedModeBanner: false,
        home: Scaffold(
            key: scaffoldKey,
            backgroundColor: Colors.white,
            appBar: AppBar(
              title: Text("발곰이",style: TextStyle(color: Colors.white)),
              centerTitle: true,
              elevation: 0.0,
            ),
            drawer: Drawer(
              child: ListView(
                children: <Widget>[
                  DrawerHeader(
                    child: Center(
                        child: Text(
                          'M e n u',
                          style: TextStyle(fontSize:35),
                        )),
                  ),
                  ListTile(
                      leading: Icon(Icons.settings,
                        color: Colors.grey[850],),
                      title: Text('설정', style: TextStyle(fontSize:20)),
                      onTap: () {
                        initSetting();
                        flutterTts.speak("설정창으로 이동합니다.");
                        Navigator.of(context).push(MaterialPageRoute(builder: (context)=> FirstPage()));
                      }
                  ),
                ],
              ),
            ),
            body: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: <Widget>[
                connectArea(),
                messageListArea(),
                submitArea(),
                directionArea(),
              ],
            ))
    );
  }


  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      connectToServer();
    });
  }

  @override
  void dispose() {
    disconnectFromServer();
    super.dispose();
  }

  Widget connectArea() {
    return Center(
      child: Container(
        child: ElevatedButton(
          child: Text((clientSocket != null) ?((runstop=="run")? "Stop" : "Run"): "Connect", style: TextStyle(color: Colors.white,fontSize: 40)),
          style: ElevatedButton.styleFrom(
              primary : ((clientSocket != null) ? ((runstop=="run")? Colors.redAccent : Colors.blueAccent): Colors.grey),
              padding: const EdgeInsets.fromLTRB(105, 80, 105, 80)
          ),
          onPressed:
          ((clientSocket != null) ? ((runstop=="run")? submitStopMessage : submitRunMessage): connectToServer),
        ),
      ),
    );
  }

  Widget messageListArea() {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Container(
          padding: const EdgeInsets.all(20.0),
          decoration: BoxDecoration(
              color: Colors.blueGrey[50],
              borderRadius: BorderRadius.circular(30)
          ),
          child: ListView.builder(
              reverse: true,
              itemCount: items.length,
              itemBuilder: (context, index) {
                MessageItem item = items[index];
                return Container(
                  alignment: Alignment.centerRight,
                  child: Container(
                    margin: const EdgeInsets.all(10),
                    padding:
                    const EdgeInsets.symmetric(vertical: 10, horizontal: 10),
                    decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(10),
                        color: Colors.blue[100]
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: <Widget>[
                        Text(
                          item.content,
                          style: TextStyle(fontSize: 18),
                        ),
                      ],
                    ),
                  ),
                );
              }),
        ),
      ),
    );
  }

  Widget submitArea() {
    return Center(
      child: Container(
        child: ElevatedButton(
          child: Text((clientSocket != null) ? ((ocrrunstop=="ocrrun")? "Stop OCR" : "Run OCR") : "Connect", style: TextStyle(color: Colors.white,fontSize: 40)),
          style: ElevatedButton.styleFrom(
              primary : ((clientSocket != null) ? ((ocrrunstop=="ocrrun")? Colors.redAccent : Colors.blueAccent): Colors.grey),
              padding: EdgeInsets.fromLTRB(95, 80, 95, 80)
          ),
          onPressed:
          (clientSocket != null) ? ((ocrrunstop=="ocrrun")? submitStopOCRMessage : submitRunOCRMessage) : connectToServer,
        ),
      ),
    );
  }

  Widget directionArea() {
    return Center(
      child: Container(
        child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
            Container(
            width: 300, // 가로 설정
            height: 20,
            ),
            ElevatedButton(
              child: Text("앞", style: TextStyle(color: Colors.white,fontSize: 30)),
              style: ElevatedButton.styleFrom(
                  primary : Colors.blueAccent,
                  padding: EdgeInsets.fromLTRB(45, 40, 45, 40)
              ),
            onPressed: submitfrontMessage
            ),
            Container(
              width: 300, // 가로 설정
              height: 5,
            ),
            Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  ElevatedButton(
                      child: Text("좌", style: TextStyle(color: Colors.white,fontSize: 30)),
                      style: ElevatedButton.styleFrom(
                          primary : Colors.blueAccent,
                          padding: EdgeInsets.fromLTRB(45, 40, 45, 40)
                      ),
                      onPressed: submitleftMessage
                  ),
                  Container(
                    width: 5, // 가로 설정
                    height: 5,
                  ),
                  ElevatedButton(
                      child: Text("뒤", style: TextStyle(color: Colors.white,fontSize: 30)),
                      style: ElevatedButton.styleFrom(
                          primary : Colors.blueAccent,
                          padding: EdgeInsets.fromLTRB(45, 40, 45, 40)
                      ),
                      onPressed: submitrearMessage
                  ),
                  Container(
                    width: 5, // 가로 설정
                    height: 5,
                  ),
                  ElevatedButton(
                      child: Text("우", style: TextStyle(color: Colors.white,fontSize: 30)),
                      style: ElevatedButton.styleFrom(
                          primary : Colors.blueAccent,
                          padding: EdgeInsets.fromLTRB(45, 40, 45, 40)
                      ),
                      onPressed: submitrightMessage
                  )
                ]
            )
        ]),
      ),
    );
  }


  void onDone() {
    showSnackBarWithKey("연결이 끊겼습니다.");
    initSetting();
    flutterTts.speak("연결이 끊겼습니다.");
    disconnectFromServer();
  }

  void onError(e) {
    print("onError: $e");
    showSnackBarWithKey(e.toString());
    initSetting();
    flutterTts.speak("오류가 발생하였습니다.");
    disconnectFromServer();
  }

  void disconnectFromServer() {
    print("disconnectFromServer");

    clientSocket!.close();
    setState(() {
      clientSocket = null;
    });
  }

  void submitRunMessage() {
    setState((){
      runstop="run";
      initSetting();
      flutterTts.speak("발곰이가 움직입니다.");
    });
    clientSocket!.write(runstop);
  }
  void submitStopMessage() {
    setState((){
      runstop="stop";
      initSetting();
      flutterTts.speak("발곰이를 멈췄습니다.");
    });
    clientSocket!.write("Stop");
  }
  void submitRunOCRMessage() {
    clientSocket!.write("Run OCR");
    setState(() {
      ocrrunstop = "ocrrun";
      runstop = "stop";
      initSetting();
      flutterTts.speak("문자 탐색을 시작합니다.");
    });
  }
  void submitStopOCRMessage() {
    clientSocket!.write("Stop OCR");
    setState(() {
      ocrrunstop = "ocrstop";
      initSetting();
      flutterTts.speak("문자 탐색을 종료합니다.");
    });
  }

  void submitfrontMessage() {
    clientSocket!.write("front");
    setState(() {
      initSetting();
      flutterTts.speak("앞으로 이동합니다");
    });
  }
  void submitleftMessage() {
    clientSocket!.write("left");
    setState(() {
      initSetting();
      flutterTts.speak("왼쪽으로 이동합니다");
    });
  }
  void submitrearMessage() {
    clientSocket!.write("rear");
    setState(() {
      initSetting();
      flutterTts.speak("뒤으로 이동합니다");
    });
  }
  void submitrightMessage() {
    clientSocket!.write("right");
    setState(() {
      initSetting();
      flutterTts.speak("오른쪽으로 이동합니다");
    });
  }

  void initSetting() async{
    await flutterTts.setVolume(_countProvider.volume);
    await flutterTts.setPitch(_countProvider.pitch);
    await flutterTts.setSpeechRate(_countProvider.speechRate);
  }

  showSnackBarWithKey(String message) {
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(SnackBar(
        content: Text(message),
        action: SnackBarAction(
          label: 'Done',
          onPressed: (){},
        ),
      ));
  }
}

class MessageItem {
  String owner;
  String content;

  MessageItem(this.owner, this.content);
}
