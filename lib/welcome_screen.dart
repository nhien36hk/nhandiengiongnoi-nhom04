import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_nhan_dien_giong_noi/global.dart';
import 'package:flutter_nhan_dien_giong_noi/login_screen.dart';

class WelcomeScreen extends StatefulWidget {
  const WelcomeScreen({super.key});

  @override
  State<WelcomeScreen> createState() => _WelcomeScreenState();
}

class _WelcomeScreenState extends State<WelcomeScreen> {
  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    getPref();
  }

  getPref() async {
    Timer(const Duration(seconds: 4), () {
  
        Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => LoginScreen(),
            ));
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: buttonColor,
      body: Container(
        child: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Image(
                image: AssetImage("assets/images/logo.jpg"),
              ),
              Text(
                'HUB APP',
                style: TextStyle(
                    fontFamily: 'Phosphate', color: Colors.white, fontSize: 40),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
