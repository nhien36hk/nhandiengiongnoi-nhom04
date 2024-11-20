import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_nhan_dien_giong_noi/constructor.dart';
import 'package:flutter_nhan_dien_giong_noi/global.dart';
import 'package:flutter_nhan_dien_giong_noi/main_screen.dart';
import 'package:flutter_nhan_dien_giong_noi/register_screen.dart';
import 'package:flutter_nhan_dien_giong_noi/widget/text_input.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:http/http.dart' as http;

class LoginScreen extends StatelessWidget {
  LoginScreen({super.key});

  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();


  Future<void> _login(context) async {
    final String url =  'http://172.20.10.4:5000/login'; // Địa chỉ server Flask của bạn
    final Map<String, String> headers = {"Content-Type": "application/json"};

    final Map<String, String> body = {
      "username": _emailController.text,
      "password": _passwordController.text,
    };

    try {
      final response = await http.post(Uri.parse(url),
          headers: headers, body: json.encode(body));

      if (response.statusCode == 200) {
        // Nếu đăng nhập thành công
        final Map<String, dynamic> data = json.decode(response.body);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(data['message'])),
        );

        Constructor.username = _emailController.text;

        Navigator.push(context, MaterialPageRoute(builder: (context) => MainScreen(),));
      } else {
        print(response.body);
        // Nếu đăng nhập thất bại
        final Map<String, dynamic> data = json.decode(response.body);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(data['error'])),
        );
      }
    } catch (e) {
      print("Lỗi kết nối" + e.toString());
      // Xử lý lỗi nếu không thể kết nối với API
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Lỗi kết nối: $e")),
      );
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
                  SizedBox(height: 180),
                  Row(
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
                  SizedBox(height: 40),
                  TextInput(
                    controller: _emailController,
                    text: 'Email',
                    icon: Icons.email,
                    isObscure: false,
                  ),
                  SizedBox(height: 20),
                  TextInput(
                    controller: _passwordController,
                    text: 'Password',
                    icon: Icons.key,
                    isObscure: true,
                  ),
                  SizedBox(height: 20),
                  Text(
                    'Bạn quên mật khẩu?',
                    style: TextStyle(
                      color: buttonColor,
                      fontSize: 16,
                    ),
                  ),
                  SizedBox(height: 20),
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
                            offset: Offset(0, 3),
                          ),
                        ],
                      ),
                      padding:
                          EdgeInsets.symmetric(vertical: 13, horizontal: 75),
                      child: Text(
                        'Đăng nhập',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                  SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        'Bạn không có tài khoản?',
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: 16,
                        ),
                      ),
                      SizedBox(width: 5),
                      InkWell(
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (context) => RegisterScreen()),
                          );
                        },
                        child: Text(
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
                  SizedBox(
                    height: 20,
                  ),
                  Row(
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
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  ),
                  SizedBox(
                    height: 20,
                  ),
                  Row(
                    children: [
                      Container(
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(36),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.grey
                                  .withOpacity(0.2), // Màu sắc của bóng đổ
                              spreadRadius: 7, // Kích thước mở rộng của bóng
                              blurRadius: 7, // Mờ của bóng đổ
                              offset: Offset(0,
                                  3), // Vị trí của bóng đổ (nghĩa là x và y offset)
                            ),
                          ],
                        ),
                        padding:
                            EdgeInsets.symmetric(vertical: 15, horizontal: 25),
                        child: Row(
                          children: [
                            Icon(Icons.facebook),
                            SizedBox(
                              width: 8,
                            ),
                            Text(
                              'Facebook',
                              style: TextStyle(fontSize: 17),
                            ),
                          ],
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        ),
                      ),
                      Container(
                        decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(36),
                            boxShadow: [
                              BoxShadow(
                                spreadRadius: 7,
                                blurRadius: 7,
                                color: Colors.grey.withOpacity(0.2),
                                offset: Offset(0, 3),
                              ),
                            ]),
                        padding:
                            EdgeInsets.symmetric(vertical: 15, horizontal: 25),
                        child: Row(
                          children: [
                            Icon(Icons.email),
                            SizedBox(
                              width: 30,
                            ),
                            Text(
                              'Email',
                              style: TextStyle(fontSize: 17),
                            ),
                          ],
                          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        ),
                      ),
                    ],
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  ),
                ],
              ),
            ),
          ),
        ));
  }
}
