import 'dart:async';
import 'package:flutter/material.dart';

class ColorDisplay extends StatefulWidget {
  const ColorDisplay({super.key});

  @override
  State<ColorDisplay> createState() => _ColorDisplayState();
}

class _ColorDisplayState extends State<ColorDisplay> {
  Color containerColor = Colors.red;

  Future changeColors() async{
     while (true) {
      await Future.delayed(const Duration(seconds: 3), () {
        setState(() {
          containerColor = Colors.green;
        });
      });
      await Future.delayed(const Duration(seconds: 3), () {
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
