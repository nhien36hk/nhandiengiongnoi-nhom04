import 'package:flutter/material.dart';
import 'package:flutter_nhan_dien_giong_noi/config.dart';
import 'package:flutter_nhan_dien_giong_noi/constructor.dart';
import 'package:flutter_nhan_dien_giong_noi/global.dart';
import 'package:flutter_nhan_dien_giong_noi/login_screen.dart';
import 'package:flutter_nhan_dien_giong_noi/main_screen.dart';
import 'package:flutter_nhan_dien_giong_noi/widget/text_input.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:firebase_auth/firebase_auth.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _confirmPasswordController = TextEditingController();
  bool _obscurePassword = true;
  bool _obscureConfirmPassword = true;
  final FirebaseAuth _auth = FirebaseAuth.instance;
  final GoogleSignIn _googleSignIn = GoogleSignIn();

  Future<void> register(context) async {
    try {
      final String url = '${Config.getBaseUrl()}/register';
      final Map<String, String> headers = {"Content-Type": "application/json"};

      final Map<String, String> body = {
        "email": _emailController.text.trim(),
        "password": _passwordController.text.trim(),
        "full_name": _nameController.text.trim(),
      };

      final response = await http.post(
        Uri.parse(url),
        headers: headers, 
        body: json.encode(body)
      );

      final decodedResponse = utf8.decode(response.bodyBytes);
      print("Decoded response: $decodedResponse"); // Debug log

      if (response.statusCode == 201) {
        Constructor.username = _emailController.text.trim();
        
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Đăng ký thành công, vui lòng xác nhận email để đăng nhập!')),
        );

        await Future.delayed(const Duration(seconds: 1));

        if (context.mounted) {
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => LoginScreen()),
          );
        }
      } else {
        final Map<String, dynamic> errorData = json.decode(decodedResponse);
        throw Exception(errorData['error'] ?? 'Đăng ký thất bại');
      }
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Có lỗi xảy ra: ${e.toString()}')),
        );
      }
    }
  }

  Future<void> _handleGoogleSignIn() async {
    try {
      setState(() => Constructor.updateLoading(true));
      
      // Bắt đầu quá trình đăng nhập Google
      final GoogleSignInAccount? googleUser = await _googleSignIn.signIn();
      if (googleUser == null) return;

      // Lấy thông tin xác thực
      final GoogleSignInAuthentication googleAuth = await googleUser.authentication;
      final credential = GoogleAuthProvider.credential(
        accessToken: googleAuth.accessToken,
        idToken: googleAuth.idToken,
      );

      // Đăng nhập vào Firebase
      final UserCredential userCredential = 
          await _auth.signInWithCredential(credential);
      
      // Gửi thông tin lên server của bạn
      final response = await http.post(
        Uri.parse('${Config.getBaseUrl()}/google_sign_in'),
        headers: {"Content-Type": "application/json"},
        body: json.encode({
          "email": userCredential.user?.email,
          "name": userCredential.user?.displayName,
          "uid": userCredential.user?.uid,
        }),
      );

      if (response.statusCode == 200) {
        Constructor.username = userCredential.user?.email ?? '';
        
        if (context.mounted) {
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => const MainScreen()),
          );
        }
      } else {
        throw Exception('Đăng nhập thất bại');
      }
    } catch (e) {
      print('Error during Google sign in: $e');
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Đăng nhập Google thất bại: $e')),
        );
      }
    } finally {
      setState(() => Constructor.updateLoading(false));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 25),
          child: Column(
            children: [
              const SizedBox(
                height: 98,
              ),
              const Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  Text(
                    'Tạo tài khoản',
                    style: TextStyle(
                      color: Colors.black,
                      fontWeight: FontWeight.bold,
                      fontSize: 36,
                    ),
                  ),
                ],
              ),
              const SizedBox(
                height: 40,
              ),
              TextInput(
                  controller: _nameController,
                  text: 'Full Name',
                  icon: Icons.person,
                  isObscure: false),
              const SizedBox(
                height: 20,
              ),
              TextInput(
                  controller: _emailController,
                  text: 'Email',
                  icon: Icons.email,
                  isObscure: false),
              const SizedBox(
                height: 20,
              ),
              TextField(
                controller: _passwordController,
                obscureText: _obscurePassword,
                decoration: InputDecoration(
                  hintText: 'Password',
                  prefixIcon: const Icon(Icons.key, color: buttonColor),
                  suffixIcon: IconButton(
                    icon: Icon(
                      _obscurePassword ? Icons.visibility_off : Icons.visibility,
                      color: buttonColor,
                    ),
                    onPressed: () {
                      setState(() {
                        _obscurePassword = !_obscurePassword;
                      });
                    },
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(10),
                    borderSide: BorderSide(color: Colors.grey.shade300),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(10),
                    borderSide: const BorderSide(color: buttonColor),
                  ),
                ),
              ),
              const SizedBox(height: 20),
              TextField(
                controller: _confirmPasswordController,
                obscureText: _obscureConfirmPassword,
                decoration: InputDecoration(
                  hintText: 'Confirm Password',
                  prefixIcon: const Icon(Icons.key, color: buttonColor),
                  suffixIcon: IconButton(
                    icon: Icon(
                      _obscureConfirmPassword ? Icons.visibility_off : Icons.visibility,
                      color: buttonColor,
                    ),
                    onPressed: () {
                      setState(() {
                        _obscureConfirmPassword = !_obscureConfirmPassword;
                      });
                    },
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(10),
                    borderSide: BorderSide(color: Colors.grey.shade300),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(10),
                    borderSide: const BorderSide(color: buttonColor),
                  ),
                ),
              ),
              const SizedBox(
                height: 20,
              ),
              Container(
                decoration: BoxDecoration(
                    color: buttonColor,
                    borderRadius: BorderRadius.circular(36),
                    boxShadow: [
                      BoxShadow(
                          color: Colors.blue.withOpacity(0.2),
                          blurRadius: 10,
                          spreadRadius: 7,
                          offset: const Offset(0, 3))
                    ]),
                padding: const EdgeInsets.symmetric(vertical: 13, horizontal: 75),
                child: GestureDetector(
                  onTap: () {
                    register(context);
                  },
                  child: const Text(
                    'Tạo tài khoản',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 20,
                        fontWeight: FontWeight.bold),
                  ),
                ),
              ),
              const SizedBox(
                height: 20,
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text(
                    'Bạn đã có tài khoản?',
                    style: TextStyle(
                      color: Colors.black,
                      fontSize: 16,
                    ),
                  ),
                  const SizedBox(
                    width: 5,
                  ),
                  InkWell(
                    onTap: () {
                      Navigator.pop(context);
                    },
                    child: const Text(
                      'Đăng nhập',
                      style: TextStyle(
                          color: buttonColor,
                          fontSize: 16,
                          fontWeight: FontWeight.bold),
                    ),
                  ),
                ],
              ),
              const SizedBox(
                height: 20,
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  SizedBox(
                    width: 110,
                    height: 1,
                    child: Container(
                      color: Colors.black,
                    ),
                  ),
                  Text(
                    'đăng nhập với',
                    style: TextStyle(color: buttonColor),
                  ),
                  SizedBox(
                    width: 110,
                    height: 1,
                    child: Container(
                      color: Colors.black,
                    ),
                  ),
                ],
              ),
              const SizedBox(
                height: 20,
              ),
              Container(
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(36),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.grey.withOpacity(0.2),
                      spreadRadius: 7,
                      blurRadius: 7,
                      offset: const Offset(0, 3),
                    ),
                  ],
                ),
                padding: const EdgeInsets.symmetric(vertical: 15, horizontal: 25),
                child: InkWell(
                  onTap: _handleGoogleSignIn,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Image.asset(
                        'assets/images/super g.png',
                        height: 24,
                      ),
                      SizedBox(width: 8),
                      Text(
                        'Google',
                        style: TextStyle(fontSize: 17),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
