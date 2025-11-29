import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/models/news_model.dart';

final newsProvider = Provider<List<NewsModel>>((ref) {
  return [
    NewsModel(
      id: '1',
      title: 'Ripple Applies for Banking License',
      summary: 'Ripple has officially applied for a US banking license, a move that could change the regulatory landscape.',
      prediction: 'XRP expected to gain investor confidence in the short term.',
    ),
    NewsModel(
      id: '2',
      title: 'Elon Musk Mentions Bitcoin on X',
      summary: 'Elon Musk tweeted again about the possibility of Bitcoin integration in Tesla’s payment system.',
      prediction: 'BTC may see a temporary surge in price due to hype.',
    ),
    NewsModel(
      id: '3',
      title: 'Ethereum Gas Fees Drop Significantly',
      summary: 'Ethereum Layer 2 adoption has led to a major reduction in gas fees across the network.',
      prediction: 'Neutral to positive impact on ETH usage and adoption.',
    ),
    NewsModel(
      id: '4',
      title: 'SEC Delays ETF Decision Again',
      summary: 'The SEC has postponed its decision on several Bitcoin ETF applications until further notice.',
      prediction: 'Market may react with short-term uncertainty or consolidation.',
    ),
  ];
});
