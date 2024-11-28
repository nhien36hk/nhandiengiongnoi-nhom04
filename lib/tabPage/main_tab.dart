import 'package:flutter/material.dart';
import 'package:flutter_nhan_dien_giong_noi/constructor.dart';
import 'package:flutter_nhan_dien_giong_noi/global.dart';
import 'package:flutter_tts/flutter_tts.dart';

class MainTab extends StatefulWidget {
  const MainTab({super.key});

  @override
  State<MainTab> createState() => _MainTabState();
}

class _MainTabState extends State<MainTab> {
  FlutterTts flutterTts = FlutterTts();
  bool isSpeaking = false;
  bool _isLoading = false;
  String _userMessage = Constructor.userMessage ?? "";
  String _botResponse =
      Constructor.botResponse ?? "Bot: Chào bạn! Hãy nói điều gì đó...";

  @override
  void initState() {
    super.initState();
    _initTts();

    // Đăng ký lắng nghe thay đổi
    Constructor.onUserMessageChanged = (String message) {
      setState(() {
        _userMessage = message;
      });
    };

    Constructor.onBotResponseChanged = (String response) {
      setState(() {
        _botResponse = response;
      });
    };
  }

  Future<void> _initTts() async {
    try {
      await flutterTts.setLanguage("vi-VN");
      await flutterTts.setSpeechRate(0.5);
      await flutterTts.setVolume(1.0);
      await flutterTts.setPitch(1.0);

      flutterTts.setCompletionHandler(() {
        setState(() {
          isSpeaking = false;
        });
      });
    } catch (e) {
      print("TTS Error: $e");
    }
  }

  Future<void> speak(String text) async {
    if (text.isNotEmpty) {
      setState(() {
        isSpeaking = true;
      });
      String cleanText = text.startsWith("Bot: ") ? text.substring(5) : text;
      await flutterTts.speak(cleanText);
    }
  }

  Future<void> stop() async {
    setState(() {
      isSpeaking = false;
      _isLoading = true;
    });
    await flutterTts.stop();
  }

  @override
  void dispose() {
    // Hủy đăng ký khi widget bị hủy
    Constructor.onUserMessageChanged = null;
    Constructor.onBotResponseChanged = null;
    flutterTts.stop();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
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
          const SizedBox(height: 10),
          Card(
            elevation: 2,
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: Text(
                          _botResponse,
                          style: const TextStyle(fontSize: 18),
                        ),
                      ),
                      if (_botResponse !=
                          "Bot: Chào bạn! Hãy nói điều gì đó...")
                        IconButton(
                          icon: Icon(
                            isSpeaking ? Icons.stop : Icons.volume_up,
                            color: buttonColor,
                          ),
                          onPressed: () {
                            if (isSpeaking) {
                              stop();
                            } else {
                              speak(_botResponse);
                            }
                          },
                        ),
                    ],
                  ),
                
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
