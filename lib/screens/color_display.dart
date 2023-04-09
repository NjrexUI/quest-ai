import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:quest/screens/websocket.dart';

class ColorDisplay extends StatefulWidget {
  const ColorDisplay({super.key});

  @override
  State<ColorDisplay> createState() => _ColorDisplayState();
}

class _ColorDisplayState extends State<ColorDisplay> {
  Color containerColor = Colors.red;

  final WebSocket _socket = WebSocket("ws://localhost:5000");
  final bool _isConnected = true;
  bool isInGame = false;
  bool isGestured = false;

  Future changeColors(bool isGestured) async {
    while (true) {
      if (!isInGame) {
        if (isGestured) {
          isInGame = true;
          await Future.delayed(const Duration(seconds: 3), () {});
        } else {
          setState(() {
            containerColor = Colors.white;
          });
        }
      } else {
        await Future.delayed(const Duration(seconds: 3), () {
          setState(() {
            containerColor = Colors.white;
          });
        });
        await Future.delayed(const Duration(seconds: 3), () {
          setState(() {
            containerColor = Colors.red;
          });
        });
      }
    }
  }

  @override
  void initState() {
    _socket.connect();
    changeColors(isGestured);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return _isConnected
        ? StreamBuilder(
            stream: _socket.stream,
            builder: (context, snapshot) {
              if (!snapshot.hasData) {
                return const CircularProgressIndicator();
              }

              if (snapshot.connectionState == ConnectionState.done) {
                return const Center(
                  child: Text("Connection Closed !"),
                );
              }
              Map<String, dynamic> response = json.decode(snapshot.data);
              if (response["color"] == "white") isInGame = false;
              return Column(
                children: [
                  Container(
                    color: containerColor,
                    width: double.infinity,
                    height: double.infinity,
                  ),
                  ElevatedButton(
                    onPressed: () {
                      setState(() {
                        isGestured = true;
                      });
                    },
                    child: const Text("Is playing"),
                  ),
                ],
              );
            },
          )
        : const Text("Initiate Connection");
  }
}
