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
    final highlight = const Color(0xFFA4FF78);
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
          style: theme.textTheme.titleLarge?.copyWith(
            color: accent,
            fontWeight: FontWeight.w600,
            fontSize: 18,
          ),
        ),
        actions: [
          PopupMenuButton<String>(
            icon: const Icon(Icons.more_vert, color: Colors.grey),
            color: Colors.grey[900],
            itemBuilder: (_) => const [
              PopupMenuItem(value: 'profile', child: Text('Profile Settings')),
              PopupMenuItem(value: 'logout', child: Text('Logout')),
            ],
            onSelected: (_) {},
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Title
            Center(
              child: Text(
                news.title,
                textAlign: TextAlign.center,
                style: theme.textTheme.headlineSmall?.copyWith(
                  fontWeight: FontWeight.bold,
                  color: textColor,
                  fontSize: 22,
                ),
              ),
            ),
            const SizedBox(height: 8),

            // Metadata
            Center(
              child: Text(
                'by Crypto AI • Jul 24, 2025',
                style: TextStyle(
                  fontSize: 12.5,
                  color: subtitleColor,
                ),
              ),
            ),
            const SizedBox(height: 30),

            // News Summary Header
            Row(
              children: [
                Icon(Icons.article_outlined, size: 18, color: Colors.lightGreenAccent.shade100),
                const SizedBox(width: 6),
                Text(
                  "News Summary",
                  style: theme.textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.w600,
                    color: accent,
                    fontSize: 17,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),

            // Paragraph Summary
            Text(
              "The cryptocurrency market is reacting to shifting regulations and macroeconomic trends. While Bitcoin remains stable around 30,000, altcoins such as Ethereum, Solana, and Cardano show signs of volatility amid institutional movements. Investor sentiment is cautiously optimistic, with growing attention to on-chain activity and DeFi innovations driving near-term speculation.",
              style: theme.textTheme.bodyLarge?.copyWith(
                color: textColor,
                fontSize: 15.5,
                height: 1.6,
              ),
              textAlign: TextAlign.start,
            ),

            const SizedBox(height: 30),

            // Divider
            Divider(color: Colors.white12, thickness: 1),

            const SizedBox(height: 20),

            // AI Prediction Header
            Row(
              children: [
                Icon(Icons.smart_toy_outlined, size: 18, color: Colors.lightGreenAccent.shade100),
                const SizedBox(width: 6),
                Text(
                  "AI Prediction",
                  style: theme.textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.w600,
                    color: accent,
                    fontSize: 17,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),

            // Prediction Box
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
                    blurRadius: 10,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: RichText(
                text: TextSpan(
                  style: theme.textTheme.bodyMedium?.copyWith(
                    fontSize: 15.5,
                    height: 1.55,
                    color: textColor,
                  ),
                  children: [
                    const TextSpan(text: "Our AI model anticipates that over the next 10–14 days, "),
                    TextSpan(text: "ADA, SOL, and DOT", style: TextStyle(color: highlight)),
                    const TextSpan(text: " may experience sharp price swings due to increased exchange inflows and heightened community chatter. "),
                    TextSpan(
                        text: "Solana",
                        style: TextStyle(color: highlight, fontStyle: FontStyle.italic)),
                    const TextSpan(
                        text:
                        " in particular shows signs of a bullish breakout from its current consolidation range, provided volume sustains above average levels.\n\nMeanwhile, "),
                    const TextSpan(
                        text: "Bitcoin",
                        style: TextStyle(fontWeight: FontWeight.bold)),
                    const TextSpan(
                        text:
                        " is expected to remain within a tight range between 29,800 and 31,200 unless a significant catalyst emerges."),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 30),

            // Actions
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                IconButton(
                  icon: const Icon(Icons.copy, color: Colors.white70),
                  tooltip: 'Copy Prediction',
                  onPressed: () {
                    Clipboard.setData(ClipboardData(text: news.prediction));
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Prediction copied')),
                    );
                  },
                ),
                IconButton(
                  icon: const Icon(Icons.share, color: Colors.white70),
                  tooltip: 'Share News',
                  onPressed: () {
                    // Share.share('${news.title}\n\n${news.prediction}');
                  },
                ),
                IconButton(
                  icon: const Icon(Icons.bookmark_border, color: Colors.white70),
                  tooltip: 'Save for Later',
                  onPressed: () {
                    // Save logic
                  },
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
