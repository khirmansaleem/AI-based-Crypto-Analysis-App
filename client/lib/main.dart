import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:news_analysis_app/ui/screens/home_screen.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

const supabaseUrl = '';
const supabaseKey = '';
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Supabase.initialize(
    url: supabaseUrl,
    anonKey: supabaseKey,
  );

  final prefs = await SharedPreferences.getInstance();
  final seenGetStarted = prefs.getBool('seen_get_started') ?? false;

  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      systemNavigationBarColor: Colors.black,
      systemNavigationBarIconBrightness: Brightness.light,
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
    ),
  );

  runApp(
    ProviderScope(
      child: MyApp(showGetStarted: !seenGetStarted),
    ),
  );
}

class MyApp extends StatelessWidget {
  final bool showGetStarted;

  const MyApp({super.key, required this.showGetStarted});

  @override
  Widget build(BuildContext context) {
    final darkTheme = ThemeData(
      brightness: Brightness.dark,
      scaffoldBackgroundColor: const Color(0xFF0E0E0E),
      colorScheme: const ColorScheme.dark(
        primary: Color(0xFFB2FF59), // LightGreenAccent[400]
        secondary: Color(0xFF33691E), // Deep green
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: Color(0xFF2E2E2E),
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      textTheme:
          GoogleFonts.poppinsTextTheme(ThemeData.dark().textTheme).copyWith(
        bodyMedium: const TextStyle(color: Colors.white70),
        titleMedium:
            const TextStyle(color: Colors.white, fontWeight: FontWeight.w600),
        headlineSmall:
            const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: Colors.grey[900],
        contentPadding:
            const EdgeInsets.symmetric(vertical: 14, horizontal: 16),
        hintStyle: TextStyle(color: Colors.grey[500]),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: Colors.grey.shade800),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: Colors.grey.shade700),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: Color(0xFFB2FF59)),
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: const Color(0xFFB2FF59),
          foregroundColor: Colors.black,
          padding: const EdgeInsets.symmetric(vertical: 16),
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: const Color(0xFFB2FF59),
          side: const BorderSide(color: Color(0xFFB2FF59)),
          textStyle: const TextStyle(fontWeight: FontWeight.bold),
        ),
      ),
      navigationBarTheme: const NavigationBarThemeData(
        backgroundColor: Color(0xFF1C1C1E),
        indicatorColor: Color(0xFFB2FF59),
        iconTheme: WidgetStatePropertyAll(IconThemeData(color: Colors.white70)),
        labelTextStyle:
            WidgetStatePropertyAll(TextStyle(color: Colors.white70)),
      ),
    );

    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Crypto News AI',
      themeMode: ThemeMode.dark,
      darkTheme: darkTheme,
      home: const HomeScreen(),
    );
  }
}
