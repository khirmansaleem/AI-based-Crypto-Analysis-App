class NewsModel {
  final int id;
  final String title;
  final String summary;
  final String category;
  final DateTime publishedAt;

  /// ✅ Clean, backend-guaranteed analysis text
  final String prediction;

  NewsModel({
    required this.id,
    required this.title,
    required this.summary,
    required this.category,
    required this.publishedAt,
    required this.prediction,
  });

  /// 🧠 Full analysis (detail screen)
  String get predictionText =>
      prediction.isNotEmpty ? prediction : 'No AI analysis available.';

  /// 📰 Card preview: 1–2 key bullet points only
  String get analysisSummaryForCard {
    if (prediction.isEmpty) return '';

    final match = RegExp(
      r'ANALYSIS \(KEY POINTS\):([\s\S]*?)\n\n',
    ).firstMatch(prediction);

    if (match == null) return prediction;

    final bullets = match.group(1)!
        .split('\n')
        .where((l) => l.trim().startsWith('-'))
        .take(2)
        .join('\n');

    return bullets;
  }

  /// 📉 Extract market sentiment (optional UI badge)
  String get marketSentiment {
    final match = RegExp(
      r'MARKET SENTIMENT:\n([^\n]+)',
    ).firstMatch(prediction);

    return match?.group(1)?.trim() ?? '';
  }

  /// 📊 Extract impact score (0–100) if present
  int? get impactStrength {
    final match = RegExp(
      r'IMPACT STRENGTH.*?\n(\d+)',
    ).firstMatch(prediction);

    return match != null ? int.tryParse(match.group(1)!) : null;
  }

  factory NewsModel.fromJson(Map<String, dynamic> json) {
    return NewsModel(
      id: json['id'],
      title: json['title'] ?? '',
      summary: json['summary'] ?? '',
      category: json['category'] ?? '',
      publishedAt: DateTime.parse(json['published_at']),
      prediction: json['analysis']?['prediction'] ?? '',
    );
  }
}
