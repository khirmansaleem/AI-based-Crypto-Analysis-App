class NewsModel {
  final int id;
  final String title;
  final String summary;
  final String category;
  final DateTime publishedAt;
  final String prediction;

  NewsModel({
    required this.id,
    required this.title,
    required this.summary,
    required this.category,
    required this.publishedAt,
    required this.prediction,
  });

  factory NewsModel.fromJson(Map<String, dynamic> json) {
    return NewsModel(
      id: json['id'],
      title: json['title'],
      summary: json['summary'],
      category: json['category'],
      publishedAt: DateTime.parse(json['published_at']),
      prediction: json['analysis']?['prediction'] ?? '',
    );
  }
}
