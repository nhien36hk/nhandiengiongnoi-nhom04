import 'package:flutter/material.dart';
import 'package:flutter_nhan_dien_giong_noi/global.dart';
import 'package:flutter_nhan_dien_giong_noi/widget/text_input.dart';

class RegisterScreen extends StatelessWidget {
  RegisterScreen({super.key});

  TextEditingController _nameController = TextEditingController();
  TextEditingController _emailController = TextEditingController();
  TextEditingController _passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 25),
          child: Column(
            children: [
              SizedBox(
                height: 98,
              ),
              Row(
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
                mainAxisAlignment: MainAxisAlignment.start,
              ),
               SizedBox(
                height: 40,
              ),
              TextInput(
                  controller: _nameController,
                  text: 'Full Name',
                  icon: Icons.person,
                  isObscure: false),
              SizedBox(
                height: 20,
              ),
              TextInput(
                  controller: _emailController,
                  text: 'Email',
                  icon: Icons.email,
                  isObscure: false),
              SizedBox(
                height: 20,
              ),
              TextInput(
                  controller: _passwordController,
                  text: 'Password',
                  icon: Icons.key,
                  isObscure: true),
        
              SizedBox(
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
                      offset: Offset(0, 3)
                    )
                  ]
                ),
                padding: EdgeInsets.symmetric(vertical: 13, horizontal: 75),
                child: GestureDetector(
                  onTap: (){
                  },
                  child: Text(
                    'Tạo tài khoản',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 20,
                        fontWeight: FontWeight.bold),
                  ),
                ),
              ),
              SizedBox(
                height: 20,
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text( 
                    'Bạn đã có tài khoản?',
                    style: TextStyle(
                      color: Colors.black,
                      fontSize: 16,
                    ),
                  ),
                  SizedBox(
                    width: 5,
                  ),
                  InkWell(
                    onTap: () {
                      Navigator.pop(context);
                    },
                    child: Text(
                      'Đăng nhập',
                      style: TextStyle(
                        color: buttonColor,
                        fontSize: 16,
                        fontWeight: FontWeight.bold
                      ),
                    ),
                  ),
                ],
              ),
              SizedBox(height: 20,),
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
                    padding: EdgeInsets.symmetric(vertical: 15, horizontal: 25),
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
                      ]
                    ),
                    padding: EdgeInsets.symmetric(vertical: 15, horizontal: 25),
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
    );
  }
}
