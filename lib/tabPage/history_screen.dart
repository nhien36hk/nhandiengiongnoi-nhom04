import 'package:flutter/material.dart';
import 'package:flutter_nhan_dien_giong_noi/global.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_nhan_dien_giong_noi/config.dart';
import 'package:flutter_nhan_dien_giong_noi/constructor.dart';
import 'package:intl/intl.dart';
import 'package:firebase_auth/firebase_auth.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> with AutomaticKeepAliveClientMixin {
  List<Map<String, dynamic>> historyItems = [];
  bool isLoading = true;

  @override
  bool get wantKeepAlive => false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    fetchHistory();
  }

  Future<void> fetchHistory() async {
    final User? user = FirebaseAuth.instance.currentUser;
    setState(() {
      isLoading = true;
    });

    try {
      print('Fetching history for user: $uid');
      final response = await http.get(
        Uri.parse('${Config.getBaseUrl()}/api/get_query_history/${user?.uid ?? uid}'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        if (mounted) {
          setState(() {
            historyItems = data.map<Map<String, dynamic>>((item) {
              try {
                final dateStr = item['created_at'].toString();
                final date = DateFormat("EEE, dd MMM yyyy HH:mm:ss 'GMT'").parse(dateStr);
                return {
                  'user_id': item['user_id'].toString(),
                  'question': item['question'].toString(),
                  'answer': item['answer'].toString(),
                  'created_at': date.toIso8601String(),
                };
              } catch (e) {
                print('Error parsing date: ${item['created_at']} - $e');
                return {
                  'user_id': item['user_id'].toString(),
                  'question': item['question'].toString(),
                  'answer': item['answer'].toString(),
                  'created_at': DateTime.now().toIso8601String(),
                };
              }
            }).toList();
            isLoading = false;
          });
        }
      } else {
        throw Exception('Failed to load history: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching history: $e');
      if (mounted) {
        setState(() {
          isLoading = false;
        });
      }
    }
  }

  @override
  void dispose() {
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : historyItems.isEmpty
              ? const Center(
                  child: Text(
                    'Không có lịch sử hội thoại',
                    style: TextStyle(fontSize: 16),
                  ),
                )
              : ListView.builder(
                  itemCount: historyItems.length,
                  itemBuilder: (context, index) {
                    final item = historyItems[index];
                    final DateTime createdAt = DateTime.parse(item['created_at']);
                    final String formattedDate = DateFormat('dd/MM/yyyy HH:mm').format(createdAt);

                    return Card(
                      margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      child: ExpansionTile(
                        title: Text(
                          'Q: ${item['question']}',
                          style: const TextStyle(
                            fontWeight: FontWeight.bold,
                            color: Colors.black87,
                          ),
                        ),
                        subtitle: Text(
                          formattedDate,
                          style: const TextStyle(fontSize: 12, color: Colors.grey),
                        ),
                        children: [
                          Padding(
                            padding: const EdgeInsets.all(16),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'Câu trả lời:',
                                  style: TextStyle(
                                    fontWeight: FontWeight.bold,
                                    color: Colors.black87,
                                  ),
                                ),
                                const SizedBox(height: 8),
                                Text(
                                  item['answer'],
                                  style: const TextStyle(color: Colors.black87),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    );
                  },
                ),
    );
  }
}