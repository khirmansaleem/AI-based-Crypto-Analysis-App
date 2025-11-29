import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/services/auth_service.dart';

final authProvider = Provider<AuthService>((ref) => AuthService());