import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../models/news_model.dart';

class NewsService {
  static const String baseUrl = 'http://194.29.101.18';

  Future<List<NewsModel>> fetchNews() async {
    final uri = Uri.parse('$baseUrl/api/news');

    try {
      final response = await http.get(uri);

      if (response.statusCode == 200) {
        final decoded = jsonDecode(response.body);

        if (decoded == null || decoded['data'] == null) {
          throw const FormatException('Invalid response format');
        }

        final List list = decoded['data'];

        return list
            .map((e) => NewsModel.fromJson(e as Map<String, dynamic>))
            .toList();
      }

      throw HttpException(
        'Server error: ${response.statusCode}',
        uri: uri,
      );
    } on SocketException {
      throw const SocketException('No internet connection');
    }
  }
}
