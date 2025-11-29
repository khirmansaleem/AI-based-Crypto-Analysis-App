import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';


final authServiceProvider = Provider<AuthService>((ref) => AuthService());

class AuthService {
  final _supabase = Supabase.instance.client;

  // Email/Password Login
  Future<void> login(String email, String password) async {
    final res = await _supabase.auth.signInWithPassword(
      email: email,
      password: password,
    );

    if (res.session == null || res.user == null) {
      throw Exception('Login failed: ${res.toString()}');
    }
  }

  // Email/Password Registration
  Future<void> register(String email, String password) async {
    final res = await _supabase.auth.signUp(
      email: email,
      password: password,
    );

    if (res.user == null) {
      throw Exception('Registration failed: ${res.toString()}');
    }
  }

  Future<void> logout() async {
    await _supabase.auth.signOut();
  }
}
