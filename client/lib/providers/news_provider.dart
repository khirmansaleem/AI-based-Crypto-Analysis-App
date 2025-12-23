import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/models/news_model.dart';
import '../data/services/news_service.dart';

final newsServiceProvider = Provider((ref) => NewsService());

final newsProvider = FutureProvider<List<NewsModel>>((ref) async {
  final service = ref.read(newsServiceProvider);
  return service.fetchNews();
});
