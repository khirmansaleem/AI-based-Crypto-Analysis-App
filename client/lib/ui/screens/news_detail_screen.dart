import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:news_analysis_app/data/models/news_model.dart'; // ✅ correct


class NewsDetailScreen extends StatelessWidget {
  final NewsModel news;

  const NewsDetailScreen({super.key, required this.news});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    final accent = Colors.lightGreenAccent.shade200;
    final background = const Color(0xFF121212);
    final cardBackground = const Color(0xFF1E1E1E);
    final textColor = Colors.white.withOpacity(0.95);
    final subtitleColor = Colors.grey.shade500;

    return Scaffold(
      backgroundColor: background,
      appBar: AppBar(
        elevation: 0,
        backgroundColor: background,
        centerTitle: true,
        iconTheme: const IconThemeData(color: Colors.white70),
        title: Text(
          'News Analysis',
          style: theme.textTheme.titleMedium?.copyWith(
            color: accent,
            fontWeight: FontWeight.w600,
            fontSize: 18,
          ),
        ),
      ),

      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [

            // 📰 Title
            Center(
              child: Text(
                news.title,
                textAlign: TextAlign.center,
                style: theme.textTheme.headlineSmall?.copyWith(
                  fontWeight: FontWeight.bold,
                  color: textColor,
                  fontSize: 22,
                  height: 1.35,
                ),
              ),
            ),

            const SizedBox(height: 10),

            // 🕒 Meta
            Center(
              child: Text(
                'AI-analyzed crypto news',
                style: TextStyle(
                  fontSize: 12.5,
                  color: subtitleColor,
                ),
              ),
            ),

            const SizedBox(height: 32),

            // 📄 Summary Header
            _sectionHeader(
              icon: Icons.article_outlined,
              title: 'News Summary',
              accent: accent,
              theme: theme,
            ),

            const SizedBox(height: 12),

            // 📄 Summary Text (REAL DATA)
            Text(
              news.summary,
              style: theme.textTheme.bodyLarge?.copyWith(
                color: textColor,
                fontSize: 15.5,
                height: 1.65,
              ),
            ),

            const SizedBox(height: 30),
            const Divider(color: Colors.white12),
            const SizedBox(height: 24),

            // 🤖 AI Analysis Header
            _sectionHeader(
              icon: Icons.smart_toy_outlined,
              title: 'AI Market Analysis',
              accent: accent,
              theme: theme,
            ),

            const SizedBox(height: 12),

            // 🤖 AI Prediction Card (RAW AI TEXT)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: cardBackground,
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: accent.withOpacity(0.25)),
                boxShadow: [
                  BoxShadow(
                    color: accent.withOpacity(0.08),
                    blurRadius: 12,
                    offset: const Offset(0, 6),
                  ),
                ],
              ),
              child: SelectableText(
                news.prediction,
                style: theme.textTheme.bodyMedium?.copyWith(
                  fontSize: 15.5,
                  height: 1.65,
                  color: textColor,
                ),
              ),
            ),

            const SizedBox(height: 32),

            // 🔘 Actions
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                IconButton(
                  icon: const Icon(Icons.copy, color: Colors.white70),
                  tooltip: 'Copy AI analysis',
                  onPressed: () {
                    Clipboard.setData(
                      ClipboardData(text: news.prediction),
                    );
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('AI analysis copied')),
                    );
                  },
                ),
                IconButton(
                  icon: const Icon(Icons.share, color: Colors.white70),
                  tooltip: 'Share',
                  onPressed: () {
                    // Share.share('${news.title}\n\n${news.prediction}');
                  },
                ),
                IconButton(
                  icon: const Icon(Icons.bookmark_border, color: Colors.white70),
                  tooltip: 'Save',
                  onPressed: () {
                    // Future feature
                  },
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  // 🔹 Section Header Widget
  Widget _sectionHeader({
    required IconData icon,
    required String title,
    required Color accent,
    required ThemeData theme,
  }) {
    return Row(
      children: [
        Icon(icon, size: 18, color: accent.withOpacity(0.9)),
        const SizedBox(width: 8),
        Text(
          title,
          style: theme.textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.w600,
            color: accent,
            fontSize: 17,
          ),
        ),
      ],
    );
  }
}
