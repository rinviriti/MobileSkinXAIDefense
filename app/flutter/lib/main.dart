import 'package:material_ui/material_ui.dart';
import 'screens/home_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MobileSkinXAIApp());
}

class MobileSkinXAIApp extends StatelessWidget {
  const new({super.key});

  @override
  Widget build(BuildContext context) {
    const primaryColor = Color(0xFF176B65);

    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'MobileSkinXAI',
      theme: ThemeData(
        useMaterial3: true,
        scaffoldBackgroundColor: const Color(0xFFF8FAF9),
        colorScheme: ColorScheme.fromSeed(
          seedColor: primaryColor,
          primary: primaryColor,
          surface: Colors.white,
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFFF8FAF9),
          elevation: 0,
          centerTitle: false,
        ),
        filledButtonTheme: FilledButtonThemeData(
          style: FilledButton.styleFrom(
            minimumSize: const Size.fromHeight(52),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(14),
            ),
          ),
        ),
      ),
      // Bridge legacy Material theme/localizations in third-party widgets.
      builder: (BuildContext context, Widget? child) {
        // ignore: deprecated_member_use
        return MaterialUiCompatibilityBridge(child: child!);
      },
      home: const HomeScreen(),
    );
  }
}
