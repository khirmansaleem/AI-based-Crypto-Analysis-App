import 'package:dio/dio.dart';
import '../models/news_model.dart';

class ApiService {
  final Dio _dio = Dio(BaseOptions(baseUrl: 'https://your-backend-url.com'));

  Future<List<NewsModel>> fetchNews() async {
    final response = await _dio.get('/news');
    return (response.data as List)
        .map((e) => NewsModel.fromJson(e))
        .toList();
  }
}