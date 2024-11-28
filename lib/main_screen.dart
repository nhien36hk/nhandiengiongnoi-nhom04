import 'package:flutter/material.dart';
import 'package:flutter_nhan_dien_giong_noi/global.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_nhan_dien_giong_noi/config.dart';
import 'package:flutter_nhan_dien_giong_noi/services/sse_service.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:flutter_nhan_dien_giong_noi/constructor.dart';
import 'package:firebase_auth/firebase_auth.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int currentIndex = 0;
  final stt.SpeechToText _speech = stt.SpeechToText();

  bool _isListening = false;
  String _userMessage = "";
  String _botResponse = "Bot: Chào bạn! Hãy nói điều gì đó...";
  String _currentResponse = "";
  bool _isBotTyping = false; // Track bot typing state
  bool _isLoading = false;
  FlutterTts flutterTts = FlutterTts();
  bool isSpeaking = false;

  @override
  void initState() {
    super.initState();
  }

  void _listen() async {
    if (!_isListening) {
      bool available = await _speech.initialize();
      if (available) {
        setState(() => _isListening = true);
        _speech.listen(
          onResult: (val) {
            setState(() {
              _userMessage = val.recognizedWords;
              Constructor.updateUserMessage(_userMessage);
            });
          },
          localeId: "vi_VN",
        );
      }
    } else {
      setState(() => _isListening = false);
      _speech.stop();
      _sendMessageToBot(_userMessage);
    }
  }

  Future<void> _sendMessageToBot(String userMessage) async {
    Constructor.updateLoading(true);
    setState(() {
      _currentResponse = "";
      _botResponse = "";
      _isBotTyping = true; // Start showing the progress indicator
    });

    try {
      final User? user = FirebaseAuth.instance.currentUser;
      print("UID" + (user?.uid ?? ""));
      // print("USERID" + (user?.uid ?? ""));
      await for (final response in SSEService.streamResponse(userMessage, user?.uid ?? uid)) {
        setState(() {
          _currentResponse += response;
          _botResponse = "Bot: $_currentResponse";
          Constructor.updateBotResponse(_botResponse);
        });
      }
    } catch (e) {
      setState(() {
        _botResponse = "Bot: Xin lỗi, tôi không thể trả lời lúc này. Lỗi: $e";
        Constructor.updateBotResponse(_botResponse);
      });
    } finally {
      Constructor.updateLoading(false);
      setState(() {
        _isBotTyping = false; // Stop the progress indicator once done
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
        automaticallyImplyLeading: false,
        backgroundColor: buttonColor,
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _listen,
        backgroundColor: buttonColor,
        child: Icon(_isListening ? Icons.mic : Icons.mic_none),
      ),
      body: Column(
        children: [
          if (_isBotTyping) const LinearProgressIndicator(color: Colors.black54,),
          Expanded(child: PageTab[currentIndex]),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: currentIndex,
        onTap: (index) {
          setState(() {
            currentIndex = index;
          });
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home, ),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.history, ),
            label: 'History',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person, ),
            label: 'Profile',
          ),
        ],
        selectedLabelStyle: const TextStyle(color: Colors.black),
        unselectedLabelStyle: const TextStyle(color: Colors.grey),
        selectedItemColor: buttonColor,
        unselectedItemColor: Colors.grey,
      ),
    );
  }
}