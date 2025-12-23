import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/news_model.dart';

class NewsService {
  static const String baseUrl = 'https://YOUR_HOSTHATCH_DOMAIN';

  Future<List<NewsModel>> fetchNews() async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/news'),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to load news');
    }

    final decoded = jsonDecode(response.body);
    final List data = decoded['data'];

    return data.map((e) => NewsModel.fromJson(e)).toList();
  }
}
