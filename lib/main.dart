import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter_nhan_dien_giong_noi/constructor.dart';
import 'package:flutter_nhan_dien_giong_noi/login_screen.dart';
import 'package:flutter_nhan_dien_giong_noi/main_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  
  Constructor.username = "";
  Constructor.isListening = false;
  Constructor.userMessage = "";
  Constructor.botResponse = "Bot: Chào bạn! Hãy nói điều gì đó...";
  
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      initialRoute: '/',
      routes: {
        '/': (context) => LoginScreen(),
        '/main': (context) => const MainScreen(),
      },
      onUnknownRoute: (settings) {
        return MaterialPageRoute(
          builder: (context) => LoginScreen(),
        );
      },
    );
  }
}