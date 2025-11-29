import 'package:flutter/material.dart';
import 'package:news_analysis_app/data/models/news_model.dart';
import '../../providers/auth_provider.dart';
import '../widgets/news_card.dart';
import 'news_detail_screen.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'login_screen.dart'; // Needed for navigation after logout


class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final newsList = List.generate(20, (index) {
      return NewsModel(
        id: '$index',
        title: 'Crypto Insight #$index: Market Trend Analysis',
        summary: 'Experts predict major altcoin movements ahead of upcoming regulations.',
        prediction: 'ADA, SOL, and DOT may show high volatility. BTC likely remains stable.',
      );
    });

    final accent = Colors.lightGreenAccent.shade200;
    final background = const Color(0xFF121212);

    return Scaffold(
      backgroundColor: background,
      appBar: AppBar(
        elevation: 0,
        backgroundColor: background,
        centerTitle: true,
        toolbarHeight: 56,
        title: Text(
          'Crypto News AI',
          style: TextStyle(
            fontSize: 22,
            fontWeight: FontWeight.bold,
            color: accent,
            letterSpacing: 0.5,
          ),
        ),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 8.0),
            child: PopupMenuButton<String>(
              icon: const Icon(
                Icons.more_vert,
                color: Colors.grey, // ✅ More subdued than accent
              ),
              position: PopupMenuPosition.under,
              offset: const Offset(0, 12),
              color: Colors.grey[900],
              elevation: 6,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              onSelected: (value) async {
                if (value == 'logout') {
                  await ref.read(authProvider).logout();
                  Navigator.pushAndRemoveUntil(
                    context,
                    MaterialPageRoute(builder: (_) => const LoginScreen()),
                        (route) => false,
                  );
                }
              },
              itemBuilder: (context) => const [
                PopupMenuItem(value: 'profile', child: Text('Profile Settings')),
                PopupMenuItem(value: 'logout', child: Text('Logout')),
              ],
            ),
          ),
        ],

      ),
      body: Column(
        children: [
          const SizedBox(height: 28), // Spacing below AppBar
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0),
            child: Row(
              children: [
                // Search field with suffix icon
                Expanded(
                  flex: 5,
                  child: Container(
                    height: 45,
                    decoration: BoxDecoration(
                      color: const Color(0xFF2A2A2A),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: TextField(
                      style: const TextStyle(color: Colors.white),
                      decoration: InputDecoration(
                        hintText: 'Search news...',
                        hintStyle: const TextStyle(color: Colors.grey),
                        suffixIcon: Padding(
                          padding: const EdgeInsets.only(right: 8.0),
                          child: Icon(Icons.search, color: Colors.white70, size: 20),
                        ),
                        border: OutlineInputBorder(
                          borderSide: BorderSide.none,
                          borderRadius: BorderRadius.circular(12),
                        ),
                        contentPadding: const EdgeInsets.symmetric(horizontal: 16),
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                // Filter icon
                Container(
                  height: 45,
                  width: 45,
                  decoration: BoxDecoration(
                    color: const Color(0xFF2A2A2A),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: IconButton(
                    icon: const Icon(Icons.filter_list, color: Colors.white70, size: 20),
                    tooltip: 'Filter',
                    onPressed: () {
                      // TODO: filter logic
                    },
                  ),
                ),
                const SizedBox(width: 8),
                // Sort icon
                Container(
                  height: 45,
                  width: 45,
                  decoration: BoxDecoration(
                    color: const Color(0xFF2A2A2A),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: IconButton(
                    icon: const Icon(Icons.sort, color: Colors.white70, size: 20),
                    tooltip: 'Sort',
                    onPressed: () {
                      // TODO: sort logic
                    },
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24), // Spacing before cards
          Expanded(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: ListView.separated(
                itemCount: newsList.length,
                separatorBuilder: (_, __) => const SizedBox(height: 12),
                itemBuilder: (context, index) => NewsCard(
                  news: newsList[index],
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => NewsDetailScreen(news: newsList[index]),
                      ),
                    );
                  },
                ),
              ),
            ),
          ),
        ],
      ),





    );
  }
}
