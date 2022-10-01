import 'package:flutter/material.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:untitled/pages/provider/count_provider.dart';
import 'package:provider/provider.dart';

late FirstPageState pageState1;

class FirstPage extends StatefulWidget {//StatefulWidget
  const FirstPage({Key?key}): super(key:key);
  @override                                     //1.생성자(Constructors)가 없는 경우 기본 생성자(default constructor,SocketClient();:생성자의 이름이 클래스와 동일하고 매개변수가 없는 생성자)가 자동으로 제공된다.
  FirstPageState createState() {             //2.state 생성, widget삭제
    pageState1 = FirstPageState();
    return pageState1;
  }
}

class FirstPageState extends State<FirstPage>{
  FlutterTts flutterTts = FlutterTts();
  late CountProvider _countProvider;

  @override
  Widget build(BuildContext context){
    _countProvider = Provider.of<CountProvider>(context);
    return Scaffold(
        backgroundColor: Colors.white,
        appBar: AppBar(
            title: Text("설정",style: TextStyle(color: Colors.white)),
            centerTitle: true,
            elevation: 0.0,
            backgroundColor: Colors.amber
        ),
        body: Container(
            margin: const EdgeInsets.only(top: 20),
            child: Center(
                child: Column( children: [
                  Container(
                    margin: const EdgeInsets.only(left: 10),
                    child: Row(
                      children:[
                        const SizedBox(
                          width: 80,
                          child: Text(
                            "Volume",
                            style: TextStyle(fontSize: 17),
                          ),
                        ),
                        Slider(
                          min: 0.5,
                          max: 2.0,
                          value: _countProvider.volume,
                          onChanged: (value){
                            _countProvider.volume= value;
                          },
                        ),
                        Container(
                          margin: const EdgeInsets.only(left: 10),
                          child : Text(
                            double.parse((_countProvider.volume).toStringAsFixed(2)).toString(),
                            style: const TextStyle(fontSize: 17),),
                        )
                      ],
                    ),
                  ),
                  Container(
                    margin: const EdgeInsets.only(left: 10),
                    child: Row(
                      children:[
                        const SizedBox(
                          width: 80,
                          child: Text(
                            "Pitch",
                            style: TextStyle(fontSize: 17),
                          ),
                        ),
                        Slider(
                          min: 0.5,
                          max: 2.0,
                          value: _countProvider.pitch,
                          onChanged: (value){
                            _countProvider.pitch=value;
                          },
                        ),
                        Container(
                          margin: const EdgeInsets.only(left: 10),
                          child : Text(
                            double.parse((_countProvider.pitch).toStringAsFixed(2)).toString(),
                            style: const TextStyle(fontSize: 17),),
                        )
                      ],
                    ),
                  ),
                  Container(
                    margin: const EdgeInsets.only(left: 10),
                    child: Row(
                      children:[
                        const SizedBox(
                          width: 80,
                          child: Text(
                            "Speech Rate",
                            style: TextStyle(fontSize: 17),
                          ),
                        ),
                        Slider(
                          min: 0.0,
                          max: 1.0,
                          value: _countProvider.speechRate,
                          onChanged: (value){
                            _countProvider.speechRate=value;
                          },
                        ),
                        Container(
                          margin: const EdgeInsets.only(left: 10),
                          child : Text(
                            double.parse((_countProvider.speechRate).toStringAsFixed(2)).toString(),
                            style: const TextStyle(fontSize: 17),),
                        )
                      ],
                    ),
                  ),
                ],
                )
            )
        )
    );
  }

}
