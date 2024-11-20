import 'package:flutter/material.dart';
import 'package:flutter_nhan_dien_giong_noi/constructor.dart';
import 'package:flutter_nhan_dien_giong_noi/login_screen.dart';
import 'package:flutter_nhan_dien_giong_noi/main_screen.dart';
import 'package:flutter_nhan_dien_giong_noi/welcome_screen.dart';

void main() {
  Constructor.username = "";
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: LoginScreen(),
    );
  }
}