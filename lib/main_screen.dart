import 'package:flutter/material.dart';
import 'package:flutter_nhan_dien_giong_noi/global.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:http/http.dart' as http;
import 'dart:convert';

class MainScreen extends StatefulWidget {
  const MainScreen({Key? key}) : super(key: key);

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int cuttentIndex = 0;

  late stt.SpeechToText _speech;
  bool _isListening = false;
  String _userMessage = "";
  String _botResponse = "Bot: Chào bạn! Hãy nói điều gì đó...";

  @override
  void initState() {
    super.initState();
    _speech = stt.SpeechToText();
  }

  void _listen() async {
    if (!_isListening) {
      bool available = await _speech.initialize();
      if (available) {
        setState(() => _isListening = true);
        _speech.listen(
          onResult: (val) => setState(() {
            _userMessage = val.recognizedWords;
          }),
          localeId: "vi_VN", // Sử dụng ngôn ngữ tiếng Việt
        );
      }
    } else {
      setState(() => _isListening = false);
      _speech.stop();
      _sendMessageToBot(
          _userMessage); // Gửi tin nhắn đến bot sau khi dừng ghi âm
    }
  }

  // Hàm gửi tin nhắn đến API Flask và nhận phản hồi
  Future<void> _sendMessageToBot(String userMessage) async {
    const String flaskUrl = 'http://172.20.10.4:5000/api/get_response';

    print("Message của người nè" + userMessage);

    try {
      final response = await http.post(
        Uri.parse(flaskUrl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'user_message': userMessage}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _botResponse = "Bot: ${data['response']}";
        });
      } else {
        setState(() {
          _botResponse = "Bot không thể trả lời câu hỏi này.";
        });
      }
    } catch (e) {
      setState(() {
        _botResponse = "Lỗi khi kết nối với bot: $e";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Trợ lý ảo",
          style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
        ),
        backgroundColor: buttonColor,
      ),
      floatingActionButton: FloatingActionButton(
          onPressed: () {
            _listen();
          },
          shape: const CircleBorder(),
          child: Image.asset(_isListening
              ? "assets/images/mic_active.png"
              : "assets/images/mic.png")),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,
      bottomNavigationBar: BottomAppBar(
        elevation: 1,
        height: 60,
        color: Colors.white,
        shape: const CircularNotchedRectangle(),
        notchMargin: 10,
        clipBehavior: Clip.antiAliasWithSaveLayer,
        child: Row(
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            IconButton(
              onPressed: () {
                setState(() {
                  cuttentIndex = 0;
                });
              },
              icon: Icon(
                Icons.grid_view_outlined,
                size: 30,
                color: cuttentIndex == 0 ? buttonColor : Colors.grey.shade400,
              ),
            ),
            IconButton(
              onPressed: () {
                setState(() {
                  cuttentIndex = 1;
                });
              },
              icon: Icon(
                Icons.notifications,
                size: 30,
                color: cuttentIndex == 1 ? buttonColor : Colors.grey.shade400,
              ),
            ),
            const SizedBox(
              width: 15,
            ),
            IconButton(
              onPressed: () {
                setState(() {
                  cuttentIndex = 2;
                });
              },
              icon: Icon(
                Icons.history,
                size: 30,
                color: cuttentIndex == 2 ? buttonColor : Colors.grey.shade400,
              ),
            ),
            IconButton(
              onPressed: () {
                setState(() {
                  cuttentIndex = 3;
                });
              },
              icon: Icon(
                Icons.person,
                size: 30,
                color: cuttentIndex == 3 ? buttonColor : Colors.grey.shade400,
              ),
            ),
          ],
        ),
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (_userMessage.isNotEmpty)
            Card(
              elevation: 2,
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text(
                  "Bạn: $_userMessage",
                  style: const TextStyle(fontSize: 18),
                ),
              ),
            ),
            SizedBox(height: 10,),
          // Hiển thị phản hồi của bot
          Card(
            elevation: 2,
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                _botResponse,
                style: const TextStyle(fontSize: 18),
              ),
            ),
          ),

        ],
      ),
    );
  }
}
