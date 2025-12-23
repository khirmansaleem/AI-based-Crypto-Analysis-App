import 'package:dio/dio.dart';
import '../models/news_model.dart';

class ApiService {
  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: 'http://139.59.172.183:8000',
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
    ),
  );


  Future<List<NewsModel>> fetchNews() async {
    final response = await _dio.get('/news');
    return (response.data as List)
        .map((e) => NewsModel.fromJson(e))
        .toList();
  }
}