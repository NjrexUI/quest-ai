import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:quest/screens/color_display.dart';
import 'package:quest/screens/second_section.dart';
import 'websocket.dart';

class FirstSection extends StatefulWidget {
  const FirstSection({Key? key}) : super(key: key);

  @override
  State<FirstSection> createState() => _FirstSectionState();
}

class _FirstSectionState extends State<FirstSection> {
  final WebSocket _socket = WebSocket("ws://localhost:5000");
  bool _isConnected = false;
  void connect(BuildContext context) {
    _socket.connect();
    setState(() {
      _isConnected = true;
    });
  }

  void disconnect() {
    _socket.disconnect();
    setState(() {
      _isConnected = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white.withOpacity(0.1),
      body: Container(
        width: double.infinity,
        decoration: const BoxDecoration(
          image: DecorationImage(
            image: AssetImage("assets/images/scroll.png"),
            fit: BoxFit.cover
          ),
        ),
        padding: const EdgeInsets.symmetric(horizontal: 200, vertical: 100),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                ElevatedButton(
                  onPressed: () => connect(context),
                  child: const Text("Connect"),
                ),
                ElevatedButton(
                  onPressed: disconnect,
                  child: const Text("Disconnect"),
                ),
              ],
            ),
            const SizedBox(
              height: 50.0,
            ),
            _isConnected
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
                      //? Working for single frames
                      Map<String, dynamic> response =
                          json.decode(snapshot.data);
                      return Image.memory(
                        Uint8List.fromList(
                          base64Decode(
                            (response["first_section"].toString()),
                          ),
                        ),
                        gaplessPlayback: true,
                        excludeFromSemantics: true,
                      );
                    },
                  )
                : const Text("Initiate Connection"),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  ElevatedButton(
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => const SecondSection(),
                        ),
                      );
                    },
                    child: const Text("Go to second stage"),
                  ),
                  ElevatedButton(
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => const ColorDisplay(),
                        ),
                      );
                    },
                    child: const Text("Go to colors stage"),
                  ),
                ],
              ),
          ],
        ),
      ),
    );
  }
}
