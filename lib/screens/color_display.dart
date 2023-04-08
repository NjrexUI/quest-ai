import 'package:flutter/material.dart';

class ColorDisplay extends StatefulWidget {
  const ColorDisplay({super.key});

  @override
  State<ColorDisplay> createState() => _ColorDisplayState();
}

class _ColorDisplayState extends State<ColorDisplay> {
  Color containerColor = Colors.red;

  void changeColors() {
     while (true) {
      Future.delayed(const Duration(milliseconds: 500), () {
        setState(() {
          containerColor = Colors.green;
        });
      });
      Future.delayed(const Duration(milliseconds: 500), () {
        setState(() {
          containerColor = Colors.red;
        });
      });
    }
  }

  @override
  void initState() {
    changeColors();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: containerColor,
      width: double.infinity,
      height: double.infinity,
    );
  }
}
