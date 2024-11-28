import 'dart:convert';

import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter_nhan_dien_giong_noi/config.dart';
import 'package:flutter_nhan_dien_giong_noi/constructor.dart';
import 'package:flutter_nhan_dien_giong_noi/global.dart';
import 'package:flutter_nhan_dien_giong_noi/main_screen.dart';
import 'package:flutter_nhan_dien_giong_noi/register_screen.dart';
import 'package:flutter_nhan_dien_giong_noi/widget/text_input.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:http/http.dart' as http;

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  bool _obscurePassword = true;
  final GoogleSignIn _googleSignIn = GoogleSignIn();
  final FirebaseAuth _auth = FirebaseAuth.instance;

  Future<void> _login(context) async {
    final String url =
        '${Config.getBaseUrl()}/login'; // Địa chỉ server Flask của bạn
    final Map<String, String> headers = {"Content-Type": "application/json"};

    final Map<String, String> body = {
      "email": _emailController.text,
      "password": _passwordController.text,
    };

    try {
      final response = await http.post(Uri.parse(url),
          headers: headers, body: json.encode(body));

      if (response.statusCode == 200) {
        // Nếu đăng nhập thành công
        final Map<String, dynamic> data = json.decode(response.body);
        uid = data['user_id'];
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(data['message'])),
        );

        Constructor.username = _emailController.text;

        Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => const MainScreen(),
            ));
      } else {
        print(response.body);
        // Nếu đăng nhập thất bại
        final Map<String, dynamic> data = json.decode(response.body);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(data['error'])),
        );
      }
    } catch (e) {
      print("Lỗi kết nối$e");
      // Xử lý lỗi nếu không thể kết nối với API
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Lỗi kết nối: $e")),
      );
    }
  }

  Future<void> _handleGoogleSignIn() async {
    try {
      setState(() => Constructor.updateLoading(true));

      // Luôn yêu cầu người dùng chọn tài khoản
      final GoogleSignInAccount? googleUser = await _googleSignIn.signIn();
      if (googleUser == null) return;

      // Lấy thông tin xác thực
      final GoogleSignInAuthentication googleAuth = await googleUser.authentication;
      final credential = GoogleAuthProvider.credential(
        accessToken: googleAuth.accessToken,
        idToken: googleAuth.idToken,
      );

      // Đăng nhập vào Firebase
      final UserCredential userCredential = await _auth.signInWithCredential(credential);

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
      print("Error signing in with Google: $e");
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
        body: GestureDetector(
          onTap: () {
            FocusScope.of(context).unfocus();
          },
          child: SingleChildScrollView(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 25),
              child: Column(
                children: [
                  const SizedBox(height: 180),
                  const Row(
                    mainAxisAlignment: MainAxisAlignment.start,
                    children: [
                      Text(
                        'Đăng nhập',
                        style: TextStyle(
                          color: Colors.black,
                          fontWeight: FontWeight.bold,
                          fontSize: 36,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 40),
                  TextInput(
                    controller: _emailController,
                    text: 'Email',
                    icon: Icons.email,
                    isObscure: false,
                  ),
                  const SizedBox(height: 20),
                  TextField(
                    controller: _passwordController,
                    obscureText: _obscurePassword,
                    decoration: InputDecoration(
                      hintText: 'Password',
                      prefixIcon: const Icon(Icons.key, color: buttonColor),
                      suffixIcon: IconButton(
                        icon: Icon(
                          _obscurePassword
                              ? Icons.visibility_off
                              : Icons.visibility,
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
                  const Text(
                    'Bạn quên mật khẩu?',
                    style: TextStyle(
                      color: buttonColor,
                      fontSize: 16,
                    ),
                  ),
                  const SizedBox(height: 20),
                  GestureDetector(
                    onTap: () {
                      _login(context); // Gọi hàm đăng nhập khi nhấn nút
                    },
                    child: Container(
                      decoration: BoxDecoration(
                        color: buttonColor,
                        borderRadius: BorderRadius.circular(36),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.blue.withOpacity(0.2),
                            blurRadius: 10,
                            spreadRadius: 7,
                            offset: const Offset(0, 3),
                          ),
                        ],
                      ),
                      padding:
                          const EdgeInsets.symmetric(vertical: 13, horizontal: 75),
                      child: const Text(
                        'Đăng nhập',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text(
                        'Bạn không có tài khoản?',
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: 16,
                        ),
                      ),
                      const SizedBox(width: 5),
                      InkWell(
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (context) => RegisterScreen()),
                          );
                        },
                        child: const Text(
                          'Tạo tài khoản',
                          style: TextStyle(
                            color: buttonColor,
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
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
                  Row(
                    children: [
                      Expanded(
                        child: Container(
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
                          padding:
                              const EdgeInsets.symmetric(vertical: 15, horizontal: 25),
                          child: InkWell(
                            onTap: _handleGoogleSignIn,
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Image.asset(
                                  'assets/images/super g.png',
                                  height: 24,
                                ),
                                const SizedBox(width: 8),
                                const Text(
                                  'Google',
                                  style: TextStyle(fontSize: 17),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ));
  }
}
