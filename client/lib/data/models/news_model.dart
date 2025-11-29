class NewsModel {
  final String id;
  final String title;
  final String summary;
  final String prediction;

  NewsModel({
    required this.id,
    required this.title,
    required this.summary,
    required this.prediction,
  });

  factory NewsModel.fromJson(Map<String, dynamic> json) => NewsModel(
    id: json['id'],
    title: json['title'],
    summary: json['summary'],
    prediction: json['prediction'],
  );
}