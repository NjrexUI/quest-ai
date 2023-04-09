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
  bool isStarted = false;
  bool isAccessible = true;
  late bool isMoving = false;

  Future changeColors() async {
    while (true) {
      if (!isStarted) {
        isAccessible = true;
        setState(() {
          containerColor = Colors.white;
        });
        await Future.delayed(const Duration(seconds: 3), () {});
      } else {
        await Future.delayed(const Duration(seconds: 3), () {
          setState(() {
            containerColor = Colors.red;
          });
        });
        await Future.delayed(const Duration(seconds: 3), () {
          setState(() {
            containerColor = Colors.white;
          });
        });
        if (isMoving) {
          isStarted = false;
        }
      }
    }
  }

  @override
  void initState() {
    _socket.connect();
    changeColors();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.transparent,
      ),
      backgroundColor: Colors.white,
      body: _isConnected
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
                isMoving = response["color"] == "white";
                return Column(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    const Text(
                      "This is the game where in order to win you have to not move. Be patient and wait!",
                      style: TextStyle(fontFamily: "Alkatra", fontSize: 24),
                    ),
                    Container(
                      color: containerColor,
                      width: double.infinity,
                      height: MediaQuery.of(context).size.height * 0.75,
                    ),
                    isAccessible
                        ? ElevatedButton(
                            onPressed: () {
                              isStarted = true;
                              isAccessible = false;
                            },
                            child: const Text("Start the game!"),
                          )
                        : Container()
                  ],
                );
              },
            )
          : const Text("Initiate Connection"),
    );
  }
}
