import 'package:flutter/material.dart';
import 'package:flutter_nhan_dien_giong_noi/constructor.dart';

class MainTab extends StatefulWidget {
  const MainTab({super.key});

  @override
  State<MainTab> createState() => _MainTabState();
}

class _MainTabState extends State<MainTab> {
  @override
  Widget build(BuildContext context) {
    return Padding(
        padding: const EdgeInsets.only(top: 10),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (Constructor.userMessage!.isNotEmpty)
              Card(

                elevation: 2,

                child: Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Text(
                    "Bạn: ${Constructor.userMessage}",
                    style: const TextStyle(fontSize: 16),
                  ),
                ),
              ),
            SizedBox(height: 10,),
            Card(
              elevation: 2,
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text(
                  Constructor.botResponse!,
                  style: const TextStyle(fontSize: 16),
                ),
              ),
            ),
            const SizedBox(height: 20),
            // Hiển thị trạng thái ghi âm
            const SizedBox(height: 20),
            // Nút bấm để ghi âm
            const SizedBox(height: 20),
            // Hiển thị tin nhắn người dùng sau khi ghi âm
          ],
        ),
      );
  }
}