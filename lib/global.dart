import 'package:flutter/material.dart';
import 'package:flutter_nhan_dien_giong_noi/tabPage/history_screen.dart';
import 'package:flutter_nhan_dien_giong_noi/tabPage/main_tab.dart';
import 'package:flutter_nhan_dien_giong_noi/tabPage/profile_screen.dart';

const buttonColor = Color(0xFF1877F2);

List<Widget> PageTab = [
  const MainTab(),
  const HistoryScreen(),
  const ProfileScreen(),
];

String uid = "";

