import 'package:http/http.dart' as http;
import 'dart:convert';
import '../config.dart';

class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();

  final String baseUrl = Config.getBaseUrl();

  Future<Map<String, dynamic>> login(String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': email,
          'password': password,
        }),
      );
      return jsonDecode(response.body);
    } catch (e) {
      throw Exception('Failed to login: $e');
    }
  }

  Future<Map<String, dynamic>> getResponse(String message) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/get_response'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'user_message': message}),
      );
      return jsonDecode(response.body);
    } catch (e) {
      throw Exception('Failed to get response: $e');
    }
  }

  // Add other API methods here...
} 