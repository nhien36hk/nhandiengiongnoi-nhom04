import 'package:firebase_auth/firebase_auth.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_nhan_dien_giong_noi/config.dart';

class SSEService {
  final User? user = FirebaseAuth.instance.currentUser;

  static Stream<String> streamResponse(String message, String? userId) async* {
    final url = Uri.parse('${Config.getBaseUrl()}/api/stream_response');
    final request = http.Request('POST', url)
      ..headers['Content-Type'] = 'application/json'
      ..headers['Accept'] = 'text/event-stream'
      ..headers['Cache-Control'] = 'no-cache'
      ..body = json.encode({'text': message, 'user_id': userId});

    final response = await http.Client().send(request);
    
    if (response.statusCode != 200) {
      throw Exception('Failed to connect to server: ${response.statusCode}');
    }

    await for (final chunk in response.stream.transform(utf8.decoder).transform(const LineSplitter())) {
      if (chunk.startsWith('data: ')) {
        final data = chunk.substring(6);
        try {
          final jsonData = json.decode(data);
          if (jsonData.containsKey('error')) {
            throw Exception(jsonData['error']);
          } else if (jsonData.containsKey('content')) {
            yield jsonData['content'];
          }
        } catch (e, stackTrace) {
          print('Error parsing JSON: $e');
          print('Chi tiết lỗi: $stackTrace');
        }
      }
    }
  }
} 