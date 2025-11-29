import 'package:flutter/material.dart';
import 'package:news_analysis_app/data/models/news_model.dart';

class NewsCard extends StatelessWidget {
  final NewsModel news;
  final VoidCallback onTap;

  const NewsCard({super.key, required this.news, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final primary = Colors.lightGreenAccent.shade200;
    final mutedAccent = Colors.lightGreenAccent.shade100;
    final blueAccent = Colors.white;
    final cardBg = const Color(0xFF1E1E1E); // Deeper tone
    final borderHighlight = primary.withOpacity(0.4);

    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        decoration: BoxDecoration(
          color: cardBg,
          borderRadius: BorderRadius.circular(12),
          border: Border(left: BorderSide(color: borderHighlight, width: 3)),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.3),
              blurRadius: 5,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        padding: const EdgeInsets.fromLTRB(16, 16, 16, 14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Title + AI Badge
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: Text(
                    news.title,
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      color: Colors.white.withOpacity(0.95),
                      fontWeight: FontWeight.w700,
                      fontSize: 17,
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                  decoration: BoxDecoration(
                    border: Border.all(color: borderHighlight),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    'AI',
                    style: TextStyle(
                      fontSize: 10,
                      color: primary,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),

            // Summary
            Text(
              news.summary,
              style: TextStyle(
                color: Colors.white70,
                fontSize: 14,
                height: 1.5,
              ),
            ),
            const SizedBox(height: 14),

            // Prediction
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Icon(Icons.trending_up, color: blueAccent, size: 18),
                const SizedBox(width: 6),
                Expanded(
                  child: Text(
                    news.prediction,
                    style: TextStyle(
                      fontStyle: FontStyle.italic,
                      color: blueAccent,
                      fontSize: 13.5,
                      height: 1.4,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),

            // Confidence Bar
            Row(
              children: [
                Text('Confidence',
                    style: TextStyle(color: Colors.grey[400], fontSize: 12)),
                const SizedBox(width: 8),
                Expanded(
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(4), // Rounded corners
                    child: LinearProgressIndicator(
                      value: 0.75,
                      minHeight: 5,
                      backgroundColor: Colors.white12,
                      valueColor: AlwaysStoppedAnimation<Color>(mutedAccent),
                    ),
                  ),
                ),

              ],
            ),
            const SizedBox(height: 8),

            // Timestamp
            Align(
              alignment: Alignment.bottomRight,
              child: Text(
                '2h ago',
                style: TextStyle(color: Colors.grey[600], fontSize: 11),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
